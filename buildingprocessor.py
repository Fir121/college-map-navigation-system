import folium
from geojson import Polygon

class Building:
    def __init__(self, map, mulLines):
        self.map = map

        for line in mulLines:
            coors = line['geometry']['coordinates']
            self.drawBuilding(coors, line['properties']['name'])

    def drawBuilding(self, coors, name):
        folium.GeoJson(Polygon(coors), name="geojson", tooltip=name).add_to(self.map)
