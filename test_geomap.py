# coding: utf-8

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon


def make_dataset():
    c = pd.read_csv('test_coordinates.csv')
    c['geometry'] = c.apply(lambda row: Point(row.lng, row.lat), axis=1)
    return gpd.GeoDataFrame(c)
   

def main():
    df = load_dataset()
    ax = df.plot()
    df.apply(lambda x: ax.annotate(s=x['name'], xy=x.geometry.coords[0], xytext=(3, 3), textcoords="offset points"), axis=1)
    plt.axis('off')
    plt.savefig('test_map_export_labelled.svg', bbox_inches='tight',transparent=True, pad_inches=0)
    
if __name__ == '__main__':
    main()
