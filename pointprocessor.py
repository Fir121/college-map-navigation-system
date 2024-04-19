import json
import folium
from geojson import Point

class Graph:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.edges = []
    
    def addEdge(self, edge):
        self.edges.append(edge)
    
    def distance(self, node):
        return ((self.x - node.x)**2 + (self.y - node.y)**2)**0.5

class PointPath:
    def __init__(self, mulLines):

        self.nodes = []
        for line in mulLines:
            cors = line['geometry']['coordinates']
            for i in range(len(cors)):
                node = Graph(cors[i][0], cors[i][1])
                if i > 0:
                    node.addEdge(self.nodes[-1])
                    self.nodes[-1].addEdge(node)
                self.nodes.append(node)

        self.thresh = 0.00001
        self.consolidatePoints()

    def getEdges(self):
        return self.nodes

    def consolidatePoints(self):
        nodes_to_delete = []
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes)):
                if i == j or i in nodes_to_delete:
                    continue
                if abs(self.nodes[i].x - self.nodes[j].x) < self.thresh and abs(self.nodes[i].y - self.nodes[j].y) < self.thresh:
                    if self.nodes[i] in self.nodes[j].edges:
                        continue
                    for edge in self.nodes[j].edges:
                        self.nodes[i].addEdge(edge)
                        edge.edges[edge.edges.index(self.nodes[j])] = self.nodes[i]
                    nodes_to_delete.append(j)
                    break
        
        for index in sorted(nodes_to_delete, reverse=True):
            del self.nodes[index]
    
    def markerPath(self, map):
        for node in self.nodes:
            folium.GeoJson(Point((node.x, node.y)), tooltip=f"{node.x},{node.y}, {len(node.edges)}").add_to(map)
