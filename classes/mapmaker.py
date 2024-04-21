import folium, json
from classes.buildingprocessor import Building
from classes.pointprocessor import PointPath

class MapBuilder:
    def __init__(self):
        BPDCLocation = (25.13207, 55.4197599)
        self.map_BPDC = folium.Map(
            location = BPDCLocation, 
            width = "100%", 
            min_zoom= 20, 
            max_zoom= 50,
            control_scale=True,
            zoom_control=True,
            min_lat=55.41909365240795,
            min_lon=25.131174419314377,
            max_lat=55.42042089292897,
            max_lon=25.132329001728706
        )

        with open("completemapping.geojson", "r") as f:
            data = json.load(f)
            features = data['features']
            polygons = [x for x in features if x['geometry']['type'] == 'Polygon']
            mulLines = [x for x in features if x['geometry']['type'] == 'LineString']

            self.b = Building(self.map_BPDC, polygons)
            self.p = PointPath(mulLines)
        