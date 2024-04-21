import streamlit as st
from classes.mapmaker import MapBuilder
from classes.pathfinder import PathFinder
import streamlit.components.v1 as components

def app(m, p):
    st.title('BPDC Navigator')
    st.write('This is a web application that helps you navigate around the BPDC campus. You can select your start and end point and the app will show you the best path to reach there.')

    buildings = m.b.buildings.keys()

    container = st.container(border=True, height=600) # to hold the map
    # dropdowns
    start_building = st.selectbox('Select your start building:', buildings, index=None)
    end_building = st.selectbox('Select your end building:', buildings, index=None)

    if start_building is None or end_building is None:
        container.write("Please select both start and end buildings.")
    elif start_building == end_building:
        container.write("You are already at your destination!")
    else:
        my_positions = p.getBuildingPoint(m.b, m.p, start_building)
        _, dist, cp = p.giveBestPath(m.map_BPDC, my_positions, m.p, m.b, end_building)
        m.map_BPDC.location = cp[::-1]
        html_string = m.map_BPDC.get_root().render().encode("utf8")

        container.write(f'You are currently at {start_building} and you want to go to {end_building}.')
        container.write('Here is the best path to reach your destination:')
        container.write(f'The distance to your destination is {dist} meters.')
        with container.container():
            components.html(html_string, height=600)

if __name__ == "__main__":
    m = MapBuilder()
    p = PathFinder()
    app(m, p)