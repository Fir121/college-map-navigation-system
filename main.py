import folium, json
from buildingprocessor import Building
from pointprocessor import PointPath

BPDCLocation = (25.13207, 55.4197599)
map_BPDC = folium.Map(location = BPDCLocation, width = "75%", zoom_start = 27, max_zoom=50)

with open("completemapping.geojson", "r") as f:
    data = json.load(f)
    features = data['features']
    polygons = [x for x in features if x['geometry']['type'] == 'Polygon']
    mulLines = [x for x in features if x['geometry']['type'] == 'LineString']

    b = Building(map_BPDC, polygons)
    p = PointPath(mulLines)
    p.markerPath(map_BPDC)

print(p.getEdges())

map_BPDC.show_in_browser()

# def switchPosition(coordinate):
#     temp = coordinate[0]
#     coordinate[0] = coordinate[1]
#     coordinate[1] = temp
#     return coordinate

# def drawPathWay(gmap, file):
#     with open(file) as f:
#         testWay = json.load(f)

#     for feature in testWay['features']:
#         path = feature['geometry']['coordinates']

#     finalPath = list(map(switchPosition,path))
#     folium.plugins.AntPath(finalPath).add_to(gmap)