#!/usr/bin/env python3
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
GeoIP2Fast - Version: v1.0.1 - 1º/Sep/2023

Author: Ricardo Abuchaim - ricardoabuchaim@gmail.com
        https://github.com/rabuchaim/geoip2fast/

License: MIT

"""
"""                                                                  
.oPYo.               o  .oPYo. .oPYo.  ooooo                 o  
8    8               8  8    8     `8  8                     8  
8      .oPYo. .oPYo. 8 o8YooP'    oP' o8oo   .oPYo. .oPYo.  o8P 
8   oo 8oooo8 8    8 8  8      .oP'    8     .oooo8 Yb..     8  
8    8 8.     8    8 8  8      8'      8     8    8   'Yb.   8  
`YooP8 `Yooo' `YooP' 8  8      8ooooo  8     `YooP8 `YooP'   8  
:....8 :.....::.....:..:..:::::.......:..:::::.....::.....:::..:
:::::8 :::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:::::..:::::::::::::::::::::::::::::::::::::::::::::::::::::::::
"""
"""
What's new in v1.0.1 - 1º/Sep/2023
    - geoip2fast.dat.gz updated with MAXMIND:GeoLite2-Country-CSV_20230901
    - improved speed in >20%! removed ipaddress module. Now we do some IP calcs.
    - new methods to set the error code for the situations PRIVATE NETWORKS and for NETWORKS NOT FOUND
      GeoIP2Fast.set_error_code_private_networks(new_value) and GeoIP2Fast.set_error_code_network_not_found(new_value)
    - new method to calculate the current speed. Returns a value of current lookups per seconds or print a formatted result.
      GeoIP2Fast.calculate_speed(print_result=True)
    - new method to calculate how many IPv4 of all internet are covered by geoip2fast.dat file. Returns a 
      percentage relative to all possible IPv4 on the internet or print a formatted result. Useful to track the changes 
      in getip2fast.dat.gz file. 
      GeoIP2Fast.calculate_coverage(print_result=True)
"""

__version__ = "1.0.1"

import sys, os, pickle, json, gzip
from struct import unpack
from random import randrange
from time import perf_counter
from functools import lru_cache
from bisect import bisect as geoipBisect
from socket import inet_aton, setdefaulttimeout, gethostbyaddr

GEOIP2FAST_DAT_GZ_FILE = os.path.join(os.path.dirname(__file__),"geoip2fast.dat.gz")

##──── Define here what do you want to return as 'country_code' if one of these errors occurs ────────────────────────────────────
GEOIP_ECCODE_PRIVATE_NETWORKS      = "--"
GEOIP_ECCODE_NETWORK_NOT_FOUND     = "--"
GEOIP_ECCODE_INVALID_IP            = ""
GEOIP_ECCODE_LOOKUP_INTERNAL_ERROR = ""
##──── ECCODE = Error Country Code ───────────────────────────────────────────────────────────────────────────────────────────────

DEFAULT_LRU_CACHE_SIZE = 1000

sys.tracebacklimit = 0

os.environ["PYTHONWARNINGS"]    = "ignore"
os.environ["PYTHONIOENCODING"]  = "UTF-8"        

reservedNetworks = {
    "0.0.0.0/8":{"01":"Reserved for self identification"},
    "10.0.0.0/8":{"02":"Private Network Class A"},
    "100.64.0.0/10":{"03":"Reserved for Shared Address Space"},
    "127.0.0.0/8":{"04":"Localhost"},
    "169.254.0.0/16":{"05":"APIPA Automatic Priv.IP Addressing"},
    "172.16.0.0/12":{"06":"Private Network Class B"},
    "192.0.0.0/29":{"07":"Reserved IANA"},
    "192.0.2.0/24":{"08":"Reserved for TEST-NET"},
    "192.88.99.0/24":{"09":"Reserved for 6to4 Relay Anycast"},
    "192.168.0.0/16":{"10":"Private Network Class C"},
    "198.18.0.0/15":{"11":"Reserved for Network Benchmark"},
    "224.0.0.0/4":{"12":"Reserved Multicast Networks"},
    "240.0.0.0/4":{"13":"Reserved for future use"}
    }

##──── Function to check the memory use under development ─────────────────────────────────────────────────────────────────────────
# def get_mem_usage()-> float:
#     import psutil
#     return psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)
    
class GeoIPError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

class GeoIPDetail(object):
    """Object to store the information obtained by searching an IP address
    """    
    def __init__(self, ip, country_code="", country_name="", cidr="", is_private=False, elapsed_time=""):
        self.ip = ip
        self.country_code = country_code
        self.country_name = country_name
        self.cidr = cidr
        self.hostname = ""
        self.is_private = is_private
        self.elapsed_time = elapsed_time
    def __str__(self):
        return f"{self.__dict__}"
    def __repr__(self):
        return f"{self.to_dict()}"
    def get_hostname(self,dns_timeout=0.1):
        """Call this function to set the property 'hostname' with a socket.gethostbyaddr(ipadr) dns lookup.

        Args:
            dns_timeout (float, optional): Defaults to 0.1.

        Returns:
            str: the hostname if success or an error message between < >
        """
        try:
            setdefaulttimeout(dns_timeout)
            result = gethostbyaddr(self.ip)[0]
            self.hostname = result if result != self.ip else ""
            return self.hostname
        except OSError as ERR:
            self.hostname = f"<{str(ERR.strerror)}>"
            return self.hostname
        except Exception as ERR:
            self.hostname = "<dns resolver error>"
            return self.hostname        
    def to_dict(self):
        """To use the result as a dict

        Returns:
            dict: a dictionary with result's properties 
        """
        d = {
            "ip": self.ip,
            "country_code": self.country_code,
            "country_name": self.country_name,
            "cidr": self.cidr,
            "hostname":self.hostname,
            "is_private": self.is_private,
            "elapsed_time": self.elapsed_time
            }
        return d
    def pp_json(self,indent=3,sort_keys=False,print_result=False):
        """ A pretty print for json

        If *indent* is a non-negative integer, then JSON array elements and object members will be pretty-printed with that indent level. An indent level of 0 will only insert newlines. None is the most compact representation.

        If *sort_keys* is true (default: False), then the output of dictionaries will be sorted by key.

        If *print_result* is True (default: False), then the output of dictionaries will be printed to stdout, otherwise a one-line string will be silently returned.

        Returns:
            string: returns a string to print.            
        """
        dump = json.dumps(self.to_dict(),sort_keys=sort_keys,indent=indent)
        if print_result == True:
            print(dump)
        return dump

class GeoIP2Fast(object):    
    """
    Creates the object that will load data from the database file and make the requested queries.

    - Usage:
        from geoip2fast import GeoIP2Fast
        
        myGeoIP = GeoIP2Fast(verbose=False,geoip2fast_data_file="")
        
        result = myGeoIP.lookup("8.8.8.8")
        
        print(result.country_code)
        
    - *geoip2fast_data_file* is used to specify a different path of file geoip2fast.dat.gz. If empty, the default paths will be used.
    
    - Returns *GEOIP_ECCODE_INVALID_IP* as country_code if the given IP is invalid

    - Returns *GEOIP_ECCODE_PRIVATE_NETWORKS* as country_code if the given IP belongs to a special/private/iana_reserved network
    
    - Returns *GEOIP_ECCODE_NETWORK_NOT_FOUND* as country_code if the network of the given IP wasn't found.

    - Returns *GEOIP_ECCODE_LOOKUP_INTERNAL_ERROR* as country_code if something eal bad occurs during the lookup function. Try again with verbose=True

    - To use the result as a dict: 
    
        result.to_dict()['country_code']
    """    
    def __init__(self, verbose=False, geoip2fast_data_file=""):
        global elapsedTimeToLocateDatabase  # declared as global to be used as elapsed time on function lookup()
        self.verbose = verbose
        if verbose == False:
            self._print_verbose = self.__print_verbose_empty

        ##──── Try to locate the database file in the directory of the application that called GeoIP2Fast ───────────────────────────
        ##──── or in the directory of the GeoIP2Fast Library ────────────────────────────────────────────────────────────────────────
        start_time = perf_counter()
        if geoip2fast_data_file != "":
            self.data_file = geoip2fast_data_file
        else:
            self.data_file = GEOIP2FAST_DAT_GZ_FILE
            try:
                databasePath = self._locate_database_file(os.path.basename(self.data_file))
                if databasePath is False:
                    raise GeoIPError("Unable to find GeoIP2Fast database file %s"%(os.path.basename(self.data_file)))
                else:
                    self.data_file = databasePath
            except Exception as ERR:
                raise GeoIPError("Unable to find GeoIP2Fast database file %s"%(os.path.basename(self.data_file)))            
        elapsedTimeToLocateDatabase = perf_counter()-start_time
        ##──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
        
        self.error_code_private_networks        = GEOIP_ECCODE_PRIVATE_NETWORKS
        self.error_code_network_not_found       = GEOIP_ECCODE_NETWORK_NOT_FOUND
        self.error_code_invalid_ip              = GEOIP_ECCODE_INVALID_IP
        self.error_code_lookup_internal_error   = GEOIP_ECCODE_LOOKUP_INTERNAL_ERROR

        self.is_loaded = False
        self._load_data(self.data_file, verbose)

    ##──── Function used to avoid "if verbose == True". The code is swaped at __init__ ───────────────────────────────────────────────
    def __print_verbose_empty(self,msg):return
    def _print_verbose(self,msg):
        print(msg,flush=True)
    ##──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    
    ##──── convert an IP address into integer ────────────────────────────────────────────────────────────────────────────────────────
    @lru_cache(maxsize=DEFAULT_LRU_CACHE_SIZE, typed=True)
    def _ip2int(self,ipaddr:str)->int:
        """
        Convert an IP Address into an integer number
        """    
        try:
            return unpack("!I", inet_aton(ipaddr))[0]
        except Exception as ERR:
            raise GeoIPError("Failed to convert the IP address (%s) to integer. %s"%(ipaddr,str(ERR)))
    ##──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

    def _locate_database_file(self,filename):
        try:
            curDir = os.path.join(os.path.abspath(os.path.curdir),filename) # path of your application
            libDir = os.path.join(os.path.dirname(__file__),filename)       # path where the library was installed
        except Exception as ERR:
            raise GeoIPError("Unable to determine the path of application %s. %s"%(filename,str(ERR)))
        try:
            os.stat(curDir).st_mode
            return curDir
        except:
            try:
                os.stat(libDir).st_mode 
                return libDir
            except Exception as ERR:
                raise GeoIPError("Unable to determine the path of library %s - %s"%(filename,str(ERR)))
            
    def _load_data(self, gzip_data_file:str, verbose=False)->bool:
        global geoipSourceInfo, geoipListFirstIP, geoipLocationsDict, geoipCountryCidr
        startTotalTime = perf_counter()
        if self.is_loaded == True:
            return True   
        try:
            try:
                inputFile = open(str(gzip_data_file).replace(".gz",""),'rb')
                self.data_file = self.data_file.replace(".gz","")
            except:
                try:
                    inputFile = gzip.open(str(gzip_data_file),'rb')
                except Exception as ERR:
                    raise GeoIPError(f"Unable to find {gzip_data_file} or {gzip_data_file} {str(ERR)}\n")
        except Exception as RR:
            raise GeoIPError(f"Failed to 'load' GeoIP2Fast! the data file {gzip_data_file} appears to be invalid or does not exist! {str(ERR)}\n")
        try:
            with inputFile:
                geoipLocationList, geoipCountryCidr, geoipListFirstIP, geoipSourceInfo = pickle.load(inputFile)
                ##──── Structure model of GeoIP2Fast dat file ────────────────────────────────────────────────────────────────────────────────────                
                # database = [locationList,       # list      "country_code:country_name"
                #             cidrList,           # list      "cidr:country_code"
                #             firstipList,        # list of integer
                #             _SOURCE_INFO        # string
                #             ]
            geoipLocationsDict = {item.split(":")[0]:item.split(":")[1] for item in geoipLocationList}
            del geoipLocationList
        except Exception as RR:
            raise GeoIPError(f"Failed to pickle the data file {gzip_data_file} {str(ERR)}\n")
        try:    # just a self test, like a warm-up, don't worry                
            [self.lookup(ip) for ip in ['1.1.1.1','90.40.30.20','180.150.200.250','240.250.150.200']]
        except Exception as ERR:
            raise GeoIPError("Failed at GeoIP2Fast warm-up... exiting...")
        self._print_verbose(f"GeoIP2Fast is ready! Database file {os.path.basename(gzip_data_file)} was loaded with %s records in %.5f seconds"%(str(len(geoipListFirstIP)),elapsedTimeToLocateDatabase+(perf_counter() - startTotalTime)))
        self.is_loaded = True
        return True

    @lru_cache(maxsize=DEFAULT_LRU_CACHE_SIZE, typed=True)
    def _bisect_lookup(self,iplong):
        try:
            return geoipBisect(geoipListFirstIP,iplong)-1
        except:
            return -1

    @lru_cache(maxsize=DEFAULT_LRU_CACHE_SIZE, typed=True)
    def _cidr_lookup(self,iplong):
        try:
            result = geoipCountryCidr[iplong]
            return (result.split(":")[0],result.split(":")[1])
        except:
            return ("","")

    @lru_cache(maxsize=DEFAULT_LRU_CACHE_SIZE, typed=True)
    def _get_num_hosts(self,CIDR):
        """Returns the number of IPs in a subnet

        Args:
            CIDR (str): A network range in CIDR representation

        Returns:
            int: number of host in a subnet network
        """
        try:
            (addr, cidr) = CIDR.split('/')
            addr = [int(x) for x in addr.split(".")]
            cidr = int(cidr)
            mask = [( ((1<<32)-1) << (32-cidr) >> i ) & 255 for i in reversed(range(0, 32, 8))]
            netw = [addr[i] & mask[i] for i in range(4)]
            bcas = [(addr[i] & mask[i]) | (255^mask[i]) for i in range(4)]
            return self._ip2int(".".join(map(str,bcas))) - self._ip2int(".".join(map(str,netw))) + 1
        except Exception as ERR:
            self._print_verbose(str(ERR))
            return 0
    
    @lru_cache(maxsize=DEFAULT_LRU_CACHE_SIZE, typed=True)
    def _get_last_ip_int(self,CIDR):
        """Returns the last IP of a network with an integer representation

        Args:
            CIDR (str): A network range in CIDR representation

        Returns:
            int: the last IP of a network converted into integer
        """
        try:
            (addr, cidr) = CIDR.split('/')
            addr = [int(x) for x in addr.split(".")]
            cidr = int(cidr)
            mask = [( ((1<<32)-1) << (32-cidr) >> i ) & 255 for i in reversed(range(0, 32, 8))]
            bcas = [(addr[i] & mask[i]) | (255^mask[i]) for i in range(4)]
            # netw = [addr[i] & mask[i] for i in range(4)]
            # self._print_verbose(addr,cidr,mask,netw,bcas,last_ip,self._ip2int(last_ip))
            # self._print_verbose("Num hosts: %d"%(self._get_num_hosts(CIDR)))
            last_ip = ".".join(map(str,bcas))
            return self._ip2int(last_ip)            
        except Exception as ERR:
            self._print_verbose(str(ERR))
            return 0
    
    @lru_cache(maxsize=500, typed=True)
    def _locations_lookup(self,country_code):
        try:
            return geoipLocationsDict[country_code]
        except:
            return ""
    
    def _get_cidr_list(self):
        """
        Returns a list of all network ranges inside the .dat file. Used to check the total IP coverage.
        """
        return [item.split(":")[0] for item in geoipCountryCidr]
    
    def set_error_code_private_networks(self,new_value)->str:
        """Change the GEOIP_ECCODE_PRIVATE_NETWORKS. This value will be returned in country_code property.

        Returns:
            str: returns the new value setted
        """
        try:
            self.error_code_private_networks = new_value
            return new_value
        except Exception as ERR:
            raise GeoIPError("Unable to set a new value for GEOIP_ECCODE_PRIVATE_NETWORKS: %s "%(str(ERR)))
        
    def set_error_code_network_not_found(self,new_value)->str:
        """Change the GEOIP_ECCODE_NETWORK_NOT_FOUND. This value will be returned in country_code property.

        Returns:
            str: returns the new value setted
        """
        try:
            self.error_code_network_not_found = new_value
            return new_value
        except Exception as ERR:
            raise GeoIPError("Unable to set a new value for GEOIP_ECCODE_NETWORK_NOT_FOUND: %s "%(str(ERR)))
        
    ##──── NO-CACHE: This function cannot be cached to don´t cache the elapsed timer. ────────────────────────────────────────────────────────────
    def lookup(self,ipaddr:str)->GeoIPDetail:
        """
        Performs a search for the given IP address in the in-memory database

        - Returns *GEOIP_ECCODE_INVALID_IP* as country_code if the given IP is invalid

        - Returns *GEOIP_ECCODE_PRIVATE_NETWORKS* as country_code if the given IP belongs to a special/private/iana_reserved network
            
        - Returns *GEOIP_ECCODE_NETWORK_NOT_FOUND* as country_code if the network of the given IP wasn't found.

        - Returns *GEOIP_ECCODE_LOOKUP_INTERNAL_ERROR* as country_code if something eal bad occurs during the lookup function. Try again with verbose=True

        - Returns an object called GeoIPDetail withm its properties: ip, country_code, country_name, cidr, hostname, is_private and elapsed_time
            
        - Usage:

            from geoip2fast import GeoIP2Fast
    
            myGeoIP = GeoIP2Fast()
            
            result = myGeoIP.lookup("8.8.8.8")
            
            print(result.country_code)

        """                    
        # 
        startTime = perf_counter()
        try:
            iplong = self._ip2int(ipaddr)
        except Exception as ERR:
            return GeoIPDetail(ipaddr,country_code=self.error_code_invalid_ip,country_name="<invalid ip address>",elapsed_time='%.9f sec'%(perf_counter()-startTime))
        try:            
            match = self._bisect_lookup(iplong=iplong)
            cidr,country_code = self._cidr_lookup(match)
            
            ##──── IF YOU COMMENT THESE 2 LINES BELOW, YOU WILL GET MUCH MORE SPEED, BUT... YOUR SEARCH ACCURACY GOES DOWN TO ~99,5% ─────────
            ##──── You can comment these 2 lines and execute the file ./tests/accuracy_check.py to see how many wrong locations could ────────
            ##──── be given in 1000000 lookups and check the difference of speed. Just for testing. ──────────────────────────────────────────
            if iplong > self._get_last_ip_int(cidr):
                return GeoIPDetail(ip=ipaddr,country_code=self.error_code_network_not_found,country_name="<network not found in database>",elapsed_time='%.9f sec'%(perf_counter()-startTime))
            ##────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
            
            country_name = self._locations_lookup(country_code)
            try:
                # On all reserved networks, we put a number as a "isocode". If is possible to convert to integer, the IP belongs to
                # a private/reserved network and does not have a country_code, so change the country_code to '--' (self.error_code_private_networks). 
                int(country_code)                                   
                country_code = self.error_code_private_networks 
                is_private = True
            except:
                is_private = False
                pass
            ##──── SUCCESS! ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────
            return GeoIPDetail(ipaddr,country_code,country_name,cidr,is_private,elapsed_time='%.9f sec'%(perf_counter()-startTime))
            ##────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
        except Exception as ERR:
            return GeoIPDetail(ip=ipaddr,country_code=self.error_code_lookup_internal_error,country_name="<internal lookup error>",elapsed_time='%.9f sec'%(perf_counter()-startTime))
    
    def clear_cache(self)->bool:
        """ 
        Clear the internal cache of the search function
        
        Return: True or False
        """
        try:
            self._bisect_lookup.cache_clear()
            self._cidr_lookup.cache_clear()
            self._get_last_ip_int.cache_clear()
            self._locations_lookup.cache_clear()
            return True
        except Exception as ERR:
            return False
        
    def cache_info(self)->str:
        """ 
        Returns information about the internal cache of main search
        
        Usage: print(GeoIP2Fast.cache_info())
        
        Exemple output: CacheInfo(hits=18, misses=29, maxsize=10000, currsize=29)
        """
        try:
            return self._bisect_lookup.cache_info()
        except Exception as ERR:
            return False
    
    def get_source_info(self):
        """
        Returns the information of the data source of geoip data.
        """
        return geoipSourceInfo
            
    def calculate_coverage(self,print_result=False)->float:
        """Calculate how many IP addresses are in all networks covered by geoip2fast.dat and compare with all 4.294.967.296 possible IPv4 addresses on the internet.
        
        Returns:
            float: Returns a percentage compared with all possible IPs.
        """
        try:
            startTime = perf_counter()
            cidrList = self._get_cidr_list()
            ipCounter = 0
            for CIDR in cidrList:
                ipCounter += self._get_num_hosts(CIDR)
            percentage = (ipCounter * 100) / 4294967296
            if print_result == True:
                print("Current IPv4 coverage: %.2f%% (%d IPs in %s networks) [%.5f sec]"%(percentage,ipCounter,len(cidrList),(perf_counter()-startTime)))
            return percentage
        except Exception as ERR:
            raise GeoIPError("Failed to calculate total IP coverage. %s"%(str(ERR)))
        
    def calculate_speed(self,print_result=False)->int:
        """Calculate how many lookups per second is possible.

        Method: generates a list of 1.000.000 of randomic IP addresses and do a GeoIP2Fast.lookup() on all IPs on this list. It tooks a few seconds, less than a minute.

        Note: This function clear all cache before start the tests. And inside the loop generates a random IP address in runtime and use the returned value to try to get closer a real situation of use. Could be 3 times faster if a list of IPs was prepared before starts the loop and did a simple lookup(IP).
        
        Returns:
            float: Returns a value of lookups per seconds.
        """
        try:
            MAX_IPS = 1000000  # ONE MILLION
            startTime = perf_counter()
            self.clear_cache()   
            # COULD BE 3X FASTER IF A LIST WITH 1.000.000 IPS WAS GENERATED BEFORE 
            # LOOKUP. BUT LET´S KEEP LIKE THIS TO GET CLOSER A REAL SITUATION OF USE
            for NUM in range(MAX_IPS):
                IP = f"{randrange(0,254)}.{randrange(0,254)}.{randrange(0,254)}.{randrange(0,254)}"
                ipinfo = self.lookup(IP)
                XXXX = ipinfo.country_code # TO SIMULATE THE USE OF THE RETURNED VALUE
            total_time_spent = perf_counter() - startTime
            current_speed = MAX_IPS / total_time_spent
            if print_result == True:
                print("Current speed: %.2f lookups per second (searched for %s IPs in %.9f seconds) [%.5f sec]"%(current_speed,MAX_IPS,total_time_spent,perf_counter()-startTime))
            return current_speed
        except Exception as ERR:
            raise GeoIPError("Failed to calculate current speed. %s"%(str(ERR)))
        
        
##──── A SIMPLE AND FAST CLI ──────────────────────────────────────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] is not None:
        GeoIP2Fast().lookup(sys.argv[1]).pp_json(print_result=True)
    else:
        print("Usage: geoip2fast <ip_address>")
