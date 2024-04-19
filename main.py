import folium, json
from buildingprocessor import Building
from pointprocessor import PointPath
from pathfinder import PathFinder

BPDCLocation = (25.13207, 55.4197599)
map_BPDC = folium.Map(
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

    b = Building(map_BPDC, polygons)
    p = PointPath(mulLines)
    # p.markerPath(map_BPDC)

    print(b.buildings.keys())

my_position = [55.41992602739069,25.131639929188452]
pf = PathFinder()
pf.giveBestPath(map_BPDC, my_position, p, b, "Sports Complex")

map_BPDC.show_in_browser()