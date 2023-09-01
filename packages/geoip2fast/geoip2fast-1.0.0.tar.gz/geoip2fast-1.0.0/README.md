# GeoIP2Fast

GeoIP2Fast is a pure-python *in memory* GeoIP country lookup library for Python 3. An IP address lookup can be as fast as 0.00003 seconds and can do over 60,000 queries per second.

With it´s own datafile (geoip2fast.dat.gz - 2.4Mb), can be loaded into memory in ~0.10 seconds and has a footprint of ~50mb of RAM for all data, so you don´t need to make requests to any webservices or connect to an external database.

This version returns only COUNTRY ISO CODE and COUNTRY NAME. There is no external dependencies, you just need the ```geoip2fast.py``` file and the data file ```geoip2fast.dat.gz```.

## Installation
```bash
pip install geoip2fast
```

# How does it work?

GeoIP2Fast has a datafile **geoip2fast.dat.gz** (2.4Mb). This file is located into the library directory (usually ```/usr/lib/python3/dist-packages/geoip2fast```), but you can place this file into the same directory of your application. The library automatically checks both paths, And the directory of your application overlaps the directory of the library. You can use an specific location also. 

The ```bisect()``` function is used together with some ordered lists of integers to search the Network/CountryCode (Yes! an IP address has an integer representation, try to ping this number: ```ping 134744072``` ).

If GeoIP2Fast does not have a network IP address that was requested, a "not found in database" error will be returned. Unlike many other libraries that when not finding a requested network, gives you the geographical location of the network immediately below. The result is not always correct.

There are network gaps in the files we use as a source of data, and these missing networks are probably addresses that those responsible have not yet declared their location. It must be remembered that the geographical accuracy is the responsibility of the network block owners. If the owner (aka ASN) of the XXX.YYY.ZZZ.D/24 network range declare that his network range is located at "Foo Island", we must believe that an IP address of that network is there.

*Don't go to Foo Island visit a girl you met on the internet just because you looked up her IP on GeoIP2Fast and the result indicated that she is there.*


# Quick Start

```
from geoip2fast import GeoIP2Fast

GEOIP = GeoIP2Fast()
result = GEOIP.lookup("200.204.0.10")
print(result)

# to use the country_code property
print(result.country_code)

# Before call the function get_hostname(), the property hostname will always be empty.
print("Hostname: "+result.hostname)
result.get_hostname()
print("Hostname: "+result.hostname)

# to work with output as a dict, use the function to_dict()
print(result.to_dict()['country_code'],result.to_dict()['country_name'])

# To pretty print the object result like json.dumps()
print(result.pp_json(indent=3,sort_keys=False))

# to check the date of the CSV files used to create the .dat file
print(GEOIP.get_source_info())

# info about internal cache
print(GEOIP.cache_info())

# clear the internal cache
print(GEOIP.clear_cache())

# to see the difference after clear cache
print(GEOIP.cache_info())
```

Once the object is created, GeoIP2Fast loads automatically all needed data into memory and has a footprint of ~50Mb of RAM. The lookup function returns an object called ```GeoIPDetail```. And you can get the values of it's properties just calling the name of proprerty: ```result.ip, result.country_code, result.country_name, result.cidr, result.is_private and result.elapsed_time```. Or use the function ```to_dict()``` to get the result as a dict.
```
{
   "ip": "8.8.8.8",
   "country_code": "US",
   "country_name": "United States",
   "cidr": "8.8.0.0/15",
   "hostname": "",
   "is_private": false,
   "elapsed_time": "0.000006763 sec"
}
```

# How fast is it?

With an virtual machine with 1 CPU and 4Gb of RAM, we have lookups **lower than 0,00005 seconds**. And if the lookup still in library´s internal cache, the elapsed time goes down to 0,000005 seconds. **GeoIP2Fast can do more than 60K queries per second, per core**  To load the datafile into memory and get ready to lookup, it tooks around 0,10 seconds. Use ```verbose=True``` to create the object GeoIP2Fast to see the spent time to start.

![](https://raw.githubusercontent.com/rabuchaim/geoip2fast/main/images/geoip2fast_test.jpg)

# geoip2fast.dat.gz file updates

Soon the script used to create the geoip2fast.dat.gz file will be included and then you will be able to update it whenever you want.

You can check the date of CSV files used to create our .dat file with the function ```get_source_info()```

```
from geoip2fast import GeoIP2Fast

MyGeoIP = GeoIP2Fast()
print(MyGeoIP.get_source_info())
```
Exemple of output:

```
MAXMIND:GeoLite2-Country-CSV_20230825
```
# Create your own GeoIP CLI with 6 lines

1. Create a file named ```geoipcli.py``` and save it in your home directory with the text below:
```
#!/usr/bin/env python3
import os, sys, geoip2fast
if len(sys.argv) > 1 and sys.argv[1] is not None:
    geoip2fast.GeoIP2Fast().lookup(sys.argv[1]).pp_json(print_result=True)
else:
    print(f"Usage: {os.path.basename(__file__)} <ip_address>")
```
2. Create a symbolic link to your new file into ```/usr/sbin``` folder, like this (let's assume that you saved the file into directory /root)
```
ln -s /root/geoipcli.py /usr/sbin/geoipcli
```
3. Now, you just need to call ```geoipcli``` from any path.
```
# geoipcli
Usage: geoip2fast <ip_address>

# geoipcli 1.2.3.4
{
   "ip": "1.2.3.4",
   "country_code": "AU",
   "country_name": "Australia",
   "cidr": "1.2.3.0/24",
   "hostname": "",
   "is_private": false,
   "elapsed_time": "0.000019727 sec"
}

# geoipcli x.y.z.w
{
   "ip": "x.y.z.w",
   "country_code": "",
   "country_name": "<invalid ip address>",
   "cidr": "",
   "hostname": "",
   "is_private": false,
   "elapsed_time": "0.000012493 sec"
}

# geoipcli 57.242.128.144
{
   "ip": "57.242.128.144",
   "country_code": "--",
   "country_name": "<network not found in database>",
   "cidr": "",
   "hostname": "",
   "is_private": true,
   "elapsed_time": "0.000019127 sec"
}
```

# GeoIP libraries that inspired me

**GeoIP2Nation - https://pypi.org/project/geoip2nation/** (Created by Avi Asher)

This library uses sqlite3 in-memory tables and use the same search concepts of GeoIP2Fast (based on search by the first´s IPs). Simple and fast! Until this date, the dump file that cames with pip install is corrupted, so use this link to download the complete SQL dump file http://www.ip2nation.com/ip2nation.zip. 

**GeoIP2 - https://pypi.org/project/geoip2/** (created by Maxmind)

This is the best library to work with Maxmind (paid subscription or with the free version). You can use http requests to Maxmind services or work with local Maxmind MMDB binary files. Pretty fast too. Sign-up to have access to all files of the free version https://dev.maxmind.com/geoip/geolite2-free-geolocation-data

**\* Maxmind is a registered trademark** - https://www.maxmind.com

# TO DO list
- a pure-python version for REDIS with a very small footprint (pure protocol, won´t use any REDIS library) **<<< On the way**
- a Flask and FastAPI code;
- a mod_geoip2fast for NGINX (kkkkk);
- a better manual, maybe at readthedocs.io;
- a version with ASN and cities;
- provide a script to update the base. If you have the paid subscription of Maxmind, you can download the files, extract into some directory and use this script to create your own geoip2fast.dat.gz file with the most complete, reliable and updated GeoIP information.

# Sugestions, bugs, wrong locations...
E-mail me: ricardoabuchaim at gmail.com
