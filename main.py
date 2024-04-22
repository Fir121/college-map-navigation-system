from classes.mapmaker import MapBuilder
from classes.pathfinder import PathFinder

m = MapBuilder()

my_position = [55.41992602739069,25.131639929188452]

pf = PathFinder()
m.p.markerPath(m.map_BPDC)
# pf.giveBestPath(m.map_BPDC, [my_position], m.p, m.b, "Auditorium")



# map_BPDC.save("map.html")
m.map_BPDC.show_in_browser()