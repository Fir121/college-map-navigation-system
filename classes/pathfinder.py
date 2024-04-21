import folium, json
from folium import plugins
from classes.pointprocessor import Graph
from shapely.geometry import shape
from shapely.geometry import Point, LineString
import heapq

class PathFinder:
    def switchPosition(self, coordinate):
        temp = coordinate[0]
        coordinate[0] = coordinate[1]
        coordinate[1] = temp
        return coordinate

    def drawPathWay(self, gmap, path):
        finalPath = list(map(self.switchPosition,path))
        folium.plugins.AntPath(finalPath).add_to(gmap)

    def getBuildingPoint(self, buildings, points, building_name):
        sp = shape(buildings.buildings[building_name]["geometry"])
        sps = []
        for point in points.nodes:
            if sp.contains(Point([point.x, point.y])):
                sps.append([point.x, point.y])
        return sps
    
    def giveBestPath(self, gmap, current_positions, points, buildings, building_name): # Main AI Method, heuristic used is Euclidean Distance. Fn takes in multiple start points (if you want to use only one start point do [start_point])
        mmpath = []
        mmdist = float("inf")
        for current_position in current_positions:
            curpos = Graph(current_position[0], current_position[1])

            # take threshold and bring to closest point in line????
            min_dist_points = 0
            min_dist = points.nodes[min_dist_points].distance(curpos)
            for i in range(1, len(points.nodes)):
                if points.nodes[i].distance(curpos) < min_dist:
                    min_dist = points.nodes[i].distance(curpos)
                    min_dist_points = i
            
            start_node = points.nodes[min_dist_points]

            building_coors = buildings.buildings[building_name]
            building_poly = shape(building_coors["geometry"])
            end_nodes = []
            for node in points.nodes:
                if building_poly.contains(Point([node.x, node.y])):
                    end_nodes.append(node)
            
            mpath = self.astar(start_node, end_nodes[0])
            mdist = self.calculateDistance(mpath)
            for i in range(1, len(end_nodes)):
                path = self.astar(start_node, end_nodes[i])
                dist = self.calculateDistance(path)
                if dist < mdist:
                    mpath = path
                    mdist = dist

            if mdist < mmdist:
                mmdist = mdist
                mmpath = mpath

        # folium.GeoJson(Point((curpos.x, curpos.y)), tooltip=f"{curpos.x},{curpos.y}").add_to(gmap)
        path = [] # not showing curpos
        for node in mmpath:
            path.append([node.x, node.y])
        self.drawPathWay(gmap, path)

        return mmdist

    def calculateDistance(self, path):
        distance = 0
        for i in range(1, len(path)):
            distance += path[i].distance(path[i-1])
        return distance
    
    def astar(self, start_node, end_node):
        frontier = []
        heapq.heappush(frontier, (0, start_node))
        came_from = dict()
        cost_so_far = dict()
        came_from[start_node] = None
        cost_so_far[start_node] = 0

        while frontier:
            current = heapq.heappop(frontier)[1]

            if current == end_node:
                break
            
            for node in current.edges:
                new_cost = cost_so_far[current] + current.distance(node)
                if node not in cost_so_far or new_cost < cost_so_far[node]:
                    cost_so_far[node] = new_cost
                    priority = new_cost + node.distance(end_node)
                    heapq.heappush(frontier, (priority, node))
                    came_from[node] = current
        else:
            raise Exception("No Path Found")
        
        path = []
        current = end_node
        while current != start_node:
            path.append(current)
            current = came_from[current]
        path.append(start_node)
        path.reverse()
        return path
