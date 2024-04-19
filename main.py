import folium
from folium import plugins
import pandas as pd

import os
import json

import datetime

BPDCLocation = (25.13207, 55.4197599)
map_BPDC = folium.Map(location = BPDCLocation, width = "75%", zoom_start = 27)

def switchPosition(coordinate):
    temp = coordinate[0]
    coordinate[0] = coordinate[1]
    coordinate[1] = temp
    return coordinate

def drawPathWay(gmap, file):
    with open(file) as f:
        testWay = json.load(f)

    for feature in testWay['features']:
        path = feature['geometry']['coordinates']

    finalPath = list(map(switchPosition,path))
    folium.plugins.AntPath(finalPath).add_to(gmap)

def drawBuilding(gmap, file):
    folium.GeoJson(file, name="geojson", tooltip=file[10:-8]).add_to(gmap)

for root, dirs, files in os.walk('locations'):
    for file in files:
        drawBuilding(map_BPDC, root+'/'+file)

for root, dirs, files in os.walk('locations/path'):
    for file in files:
        drawPathWay(map_BPDC, root+'/'+file)

map_BPDC.show_in_browser()