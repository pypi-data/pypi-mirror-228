import sys
from setuptools import setup

try:
    with open("README.md",'r') as f:
        var_longDescription = f.readlines()
    var_longDescription = "".join(var_longDescription)
         
except Exception as ERR:
    print("Erro ao ler o arquivo README.md %s"%(str(ERR)))
    sys.exit(1)

setup(
    name='geoip2fast',
    version='1.0.0',
    description='GeoIP2Fast is a pure-python *in memory* GeoIP country lookup library for Python 3',
    url='https://github.com/rabuchaim/geoip2fast',
    author='Ricardo Abuchaim',
    author_email='ricardoabuchaim@gmail.com',
    license='MIT',
    packages=['geoip2fast'],
    keywords=['geoip','geoip2','geo','maxmind','ip','geolocation','geoip2fast','geoiptoofast','ip2int','int2ip'],
    package_dir = {'geoip2fast': 'geoip2fast'},
    package_data={
        'geoip2fast': ['geoip2fast.dat.gz','tests/geoip2fast_test.py','tests/geoipcli.py'],
    },
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3.10',
    ],
    include_package_data=True,
    long_description=f"""{var_longDescription}""",
    long_description_content_type='text/markdown',    
)
