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

API_KEY = 'AIzaSyDxaM94tqzc8h5E1gxNVwOi8YDhq7TBX18'
g = GoogleV3(api_key=API_KEY)
coordinates = '../cartography/seasia_map_coordinates.csv'
location_file = '../cartography/locations.json'
base_file = '../cartography/ne_110m_land/ne_110m_land.shp'
map_file = '../cartography/seasia.svg' 
#~ def load_labels(filepath):
    #~ labels = {}
    #~ with open(filepath) as infile:
        #~ for row in csv.reader(infile):
            #~ if row[0] == 'name':
                #~ continue
            #~ name = row[0]
            #~ xpos = 5 if row[2] == '' else int(row[2])
            #~ ypos = 5 if row[3] == '' else int(row[3])
            #~ labels[name] = (xpos, ypos)
    #~ return labels
    

def make_labels(dt, ax):
    basex = 105
    prev_point = None
    xoffset = 0
    yoffset = 0
    for item in dt.sort_values('lng').itertuples():
        if not prev_point:
            prev_point = item.geometry
            continue
        if int(item.geometry.x) > basex:
            xoffset += 100
            basex = int(item.geometry.x)
            yoffset = 0
        else:
            yoffset -= 10
        
        ax.annotate(
            s=item.name, 
            xy=item.geometry.coords[0], 
            xytext=(3, 3), 
            textcoords="offset points",
            arrowprops={'arrowstyle': '-'},
            va='top',
            ha='left'
        )

        
    return True
   


#~ def make_label(ax, x):
        #~ ax.annotate(s=x['name'], 
            #~ xy=(3, 1),  
            #~ xycoords='data',
            #~ xytext=(0.8, 0.95), 
            #~ textcoords='axes fraction',
            #~ arrowprops=dict(facecolor='black', shrink=0.05),
            #~ horizontalalignment='right', 
            #~ verticalalignment='top'
        #~ )
        
def make_geoframe():
    c = pd.read_csv(coordinates)
    c['geometry'] = c.apply(lambda row: Point(row.lng, row.lat), axis=1)
    return gpd.GeoDataFrame(c)


def assemble_map():
    
    places = make_geoframe()
    #~ fig, ax = plt.subplots()
    ax = places.plot()
    places.apply(lambda x: ax.annotate(s=x['name'], xy=x.geometry.coords[0], xytext=(3, 3), textcoords="offset points"), axis=1)
    #~ base = gpd.read_file(base_file)
    #~ base.cx[90:150, -10:20].plot(ax=ax)
    #~ ax.set_aspect('equal')
    plt.rcParams['svg.fonttype'] = 'none'
    plt.axis('off')
    #~ plt.show()
    plt.savefig(map_file, transparent=True)

if __name__ == '__main__':
    assemble_map()
