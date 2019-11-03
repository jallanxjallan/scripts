# coding: utf-8

import sys
import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon



base_dir = '/home/jeremy/Desktop/natural_earth'
base_dataset = 'ne_10m_admin_0_countries.shp'
place_coordinates = '../cartography/seasia_map_coordinates.csv'

countries = ('Indonesia', 'Philippines', 'Malaysia', 'Thailand', 'Brunei', 'Cambodia', 'Vietnam', 'China')



def make_place_dataset():
    c = pd.read_csv(places)
    c['geometry'] = c.apply(lambda row: Point(row.lng, row.lat), axis=1)
    return gpd.GeoDataFrame(c)
   

def main():
    gdf = make_place_dataset()
    base = gpd.read_file(os.path.join(base_dir, base_dataset))
    fig, ax  = plt.subplots()
    ax.set_aspect('equal')
    for country in countries:
        base[base.SOVEREIGNT == country].plot(ax=ax, color='white', edgecolor='black')    

    # We can now plot our GeoDataFrame.
    gdf.plot(ax=ax, color='red')

    plt.show()
    #~ df = load_dataset()
    #~ ax = df.plot()
    #~ df.apply(lambda x: ax.annotate(s=x['name'], xy=x.geometry.coords[0], xytext=(3, 3), textcoords="offset points"), axis=1)
    #~ plt.axis('off')
    #~ plt.savefig('test_map_export_labelled.svg', bbox_inches='tight',transparent=True, pad_inches=0)
    
if __name__ == '__main__':
    main()
