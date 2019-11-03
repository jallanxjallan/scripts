#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys 
import os
import csv

sys.path.append('/home/jeremy/projects/')

from geopy.geocoders import Nominatim

locations_file = 'locations.csv'
coordinates_file = 'coordinates.csv'

def main():
    geolocator = Nominatim(user_agent="one man air force")
    with open(coordinates_file, 'w') as outfile:
        with open(locations_file) as infile:
            reader = csv.DictReader(infile)
            writer = csv.DictWriter(outfile, fieldnames=['name', 'lat', 'lng'])
            writer.writeheader()
            for row in reader:
                name = row['name']
                print('searching for ', name)
                rs = geolocator.geocode(name)
                if rs:
                    writer.writerow(dict(name=name, lat=rs.latitude, lng=rs.longitude))
                else:
                    print(name, ' not found')

if __name__ == '__main__':
    main()
