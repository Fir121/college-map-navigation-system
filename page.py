import streamlit as st
from classes.mapmaker import MapBuilder
from classes.pathfinder import PathFinder
import streamlit.components.v1 as components
from streamlit_folium import folium_static

def app(m, p):
    st.title('BPDC Navigator')
    st.write('This is a web application that helps you navigate around the BPDC campus. You can select your start and end point and the app will show you the best path to reach there.')

    buildings = m.b.buildings.keys()

    container = st.container(border=True, height=800) # to hold the map
    # dropdowns
    start_building = st.selectbox('Select your start building:', buildings, index=None)
    end_building = st.selectbox('Select your end building:', buildings, index=None)

    if start_building is None or end_building is None:
        container.header("Please select both start and end buildings.")
    elif start_building == end_building:
        container.header("You are already at your destination!")
    else:
        my_positions = p.getBuildingPoint(m.b, m.p, start_building)
        _, dist, cp = p.giveBestPath(m.map_BPDC, my_positions, m.p, m.b, end_building)
        m.map_BPDC.location = cp[::-1]

        container.header('Here is the best path to reach your destination:')
        
        col1, col2, col3 = container.columns(3)
        col1.metric("Distance", f"{dist:.2f} m")
        col2.metric("Estimated Time", f"{dist/1.5:.2f} s")
        col3.metric("Destination", end_building)
        with container.container():
            folium_static(m.map_BPDC, width=600)

if __name__ == "__main__":
    m = MapBuilder()
    p = PathFinder()
    app(m, p)