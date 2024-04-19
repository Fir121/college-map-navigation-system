import json

class Graph:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.edges = []
    
    def addEdge(self, edge):
        self.edges.append(edge)

nodes = []
with open("fullpath.geojson", "r") as f:
    mulLines = json.load(f)
    for line in mulLines['features']:
        cors = line['geometry']['coordinates']
        for i in range(len(cors)):
            node = Graph(cors[i][0], cors[i][1])
            if i > 0:
                node.addEdge(nodes[-1])
                nodes[-1].addEdge(node)
            nodes.append(node)


thresh = 0.00001
def consolidatePoints():
    nodes_to_delete = []
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i == j or i in nodes_to_delete:
                continue
            if abs(nodes[i].x - nodes[j].x) < thresh and abs(nodes[i].y - nodes[j].y) < thresh:
                if nodes[i] in nodes[j].edges:
                    continue
                print(f"Consolidating {nodes[i].x}, {nodes[i].y} and {nodes[j].x}, {nodes[j].y}, edges {len(nodes[i].edges)} and {len(nodes[j].edges)}")
                for edge in nodes[j].edges:
                    nodes[i].addEdge(edge)
                    edge.edges[edge.edges.index(nodes[j])] = nodes[i]
                nodes_to_delete.append(j)
                break
    
    for index in sorted(nodes_to_delete, reverse=True):
        del nodes[index]

consolidatePoints()




import folium
from geojson import Point

BPDCLocation = (25.13207, 55.4197599)
map_BPDC = folium.Map(location = BPDCLocation, width = "75%", zoom_start = 27)

for node in nodes:
    print(node.x, node.y, len(node.edges))
    folium.GeoJson(Point((node.x, node.y)), tooltip=f"{node.x},{node.y}, {len(node.edges)}").add_to(map_BPDC)

map_BPDC.show_in_browser()
