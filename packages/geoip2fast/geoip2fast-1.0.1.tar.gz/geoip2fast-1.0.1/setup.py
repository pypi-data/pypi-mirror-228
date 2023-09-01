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
    version='1.0.1',
    description='GeoIP2Fast is a pure python in memory GeoIP country lookup library',
    url='https://github.com/rabuchaim/geoip2fast',
    author='Ricardo Abuchaim',
    author_email='ricardoabuchaim@gmail.com',
    license='MIT',
    packages=['geoip2fast'],
    keywords=['geoip','geoip2','geoip2fast','geo','maxmind','pure-python','purepython','pure','ip','geolocation','geoiptoofast'],
    package_dir = {'geoip2fast': 'geoip2fast'},
    package_data={
        'geoip2fast': ['geoip2fast.dat.gz','geoip2fast-20230901.txt','tests/geoip2fast_test.py','tests/speed_test.py','tests/geoipcli.py'],
    },
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',  
    ],
    include_package_data=True,
    long_description=f"""{var_longDescription}""",
    long_description_content_type='text/markdown',    
)
''