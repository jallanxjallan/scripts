#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  generate_map.py
#  
#  Copyright 2018 Jeremy Allan <jeremy@Jeremyallan.com>
# 

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


base_dir = '../cartography/natural_earth'
base_dataset = 'ne_10m_admin_0_countries.shp'
places_file = '../cartography/places.csv'
countries_file = '../cartography/countries.csv'
map_file = '/home/jeremy/Desktop/one_man_air_force_map.png'

def plot_map_base(ax):
    base = gpd.read_file(os.path.join(base_dir, base_dataset))
    countries = pd.read_csv(countries_file)
    for country in countries.itertuples():
        base[base.SOVEREIGNT == country.Name].plot(ax=ax, color='white', edgecolor='black')    

    #~ for idx, row in base.iterrows():
        #~ print(row)
        #~ plt.annotate(s=row['NAME'], xy=row['coords'], horizontalalignment='center')
    

def plot_places(ax):
    c = pd.read_csv(places_file)
    c['geometry'] = c.apply(lambda row: Point(row.lng, row.lat), axis=1)
    p = gpd.GeoDataFrame(c)
    p.plot(ax=ax)
    p.apply(lambda x: ax.annotate(s=x['name'], xy=x.geometry.coords[0], xytext=(3, 3), textcoords="offset points"), axis=1)
    
def export_map():
    plt.rcParams['svg.fonttype'] = 'none'
    plt.axis('off')
    #~ plt.show()
    plt.savefig(map_file)

def assemble_map():
    fig, ax  = plt.subplots()
    ax.set_aspect('equal')
    plot_map_base(ax)
    plot_places(ax)
    export_map()
    

if __name__ == '__main__':
    assemble_map()
