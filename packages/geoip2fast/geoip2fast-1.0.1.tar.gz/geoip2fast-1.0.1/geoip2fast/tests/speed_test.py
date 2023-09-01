#!/usr/bin/env python3
# encoding: utf-8
# -*- coding: utf-8 -*-
from geoip2fast import GeoIP2Fast

GeoIP = GeoIP2Fast(verbose=True)

print("- Starting 'queries per second' test...\n")
GeoIP.calculate_speed(print_result=True)
print("")