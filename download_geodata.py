#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys 
import os
import pandas as pd
import os
import csv
from geopy import geocoders
from geopy.geocoders import GoogleV3
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
from adjustText import adjust_text

API_KEY = 'AIzaSyDxaM94tqzc8h5E1gxNVwOi8YDhq7TBX18'
g = GoogleV3(api_key=API_KEY)
place_names = '../cartography/locations.csv'
location_file = '../cartography/locations.json'
base_file = '../cartography/desa_indonesia/DesaIndonesia.shp'
map_file = '../cartography/java_test.svg'

xmin = 106
xmax = 114
ymin = -5
ymax = -10

#~ https://github.com/Phlya/adjustText/blob/master/docs/source/Examples.ipynb

def build_dataset():
    with open(place_names) as infile:
        places = pd.read_csv(infile)
    data = []
    for i, place in enumerate(places.itertuples()):
        print(place.name)
        location = g.geocode(query=place.name, region=place.region)
        if not location:
            continue
        lng = location.longitude
        lat = location.latitude
        data.append(dict(name=place.name, lng=lng, lat=lat, geometry=Point(lng, lat)))
    
    gdf = gpd.GeoDataFrame(data)
    
    gdf.to_file(location_file, driver="GeoJSON")
    



if __name__ == '__main__':
    main()
