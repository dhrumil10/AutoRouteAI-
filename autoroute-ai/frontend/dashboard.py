


# import streamlit as st
# import requests
# import folium
# from streamlit_folium import st_folium
# import urllib.parse

# if "route_coords" not in st.session_state:
#     st.session_state.route_coords = []
# if "explanation" not in st.session_state:
#     st.session_state.explanation = ""

# st.title("AutoRoute AI - Traffic Route Optimizer")

# origin = st.text_input("Origin", "Origin")
# destination = st.text_input("Destination", "Destination")
# vehicle_type = st.selectbox("Vehicle Type", ["EV", "Gasoline", "Emergency"])
# # priority = st.selectbox("Priority", ["normal", "emergency"])
# priority = st.selectbox("Priority", ["normal", "emergency", "economy"])

# def fetch_route():
#     if not origin or not destination:
#         st.error("Please enter both origin and destination.")
#         return
#     payload = {
#         "origin": origin,
#         "destination": destination,
#         "vehicle_type": vehicle_type,
#         "priority": priority,
#     }
#     try:
#         response = requests.post("http://localhost:8000/route", json=payload)
#         if response.status_code == 200:
#             data = response.json()
#             st.session_state.route_coords = data["route_coords"]
#             st.session_state.explanation = data["explanation"]
#         else:
#             st.error(f"Error from server: {response.status_code} - {response.text}")
#     except requests.exceptions.RequestException as e:
#         st.error(f"Failed to connect to backend: {e}")

# def create_google_maps_link(coords):
#     if not coords or len(coords) < 2:
#         return ""
#     origin = f"{coords[0][0]},{coords[0][1]}"
#     destination = f"{coords[-1][0]},{coords[-1][1]}"
#     waypoints = coords[1:-1]
#     waypoints_str = "|".join([f"{p[0]},{p[1]}" for p in waypoints])
#     base_url = "https://www.google.com/maps/dir/?api=1"
#     url = f"{base_url}&origin={origin}&destination={destination}"
#     if waypoints_str:
#         url += f"&waypoints={waypoints_str}"
#     url += "&travelmode=driving"
#     return url

# if st.button("Get Route"):
#     fetch_route()

# if st.session_state.route_coords:
#     # Center map on first coord
#     m = folium.Map(location=st.session_state.route_coords[0], zoom_start=14)

#     # Add start and end markers
#     folium.Marker(st.session_state.route_coords[0], popup="Origin", icon=folium.Icon(color='green')).add_to(m)
#     folium.Marker(st.session_state.route_coords[-1], popup="Destination", icon=folium.Icon(color='red')).add_to(m)

#     # Draw route polyline
#     folium.PolyLine(st.session_state.route_coords, color="blue", weight=5, opacity=0.7).add_to(m)

#     m.fit_bounds(st.session_state.route_coords)

#     st.subheader("Recommended Route Map")
#     st_folium(m, width=700, height=500)

#     st.subheader("Route Explanation")
#     st.write(st.session_state.explanation)

#     st.subheader("Estimated Energy/Fuel Consumption")
#     st.write(f"{st.session_state.estimated_consumption} {st.session_state.consumption_unit}")

#     maps_url = create_google_maps_link(st.session_state.route_coords)
#     if maps_url:
#         st.markdown(f"[Open route in Google Maps]({maps_url})", unsafe_allow_html=True)



# import streamlit as st
# import requests
# import folium
# from streamlit_folium import st_folium

# # Initialize session state variables
# if "route_coords" not in st.session_state:
#     st.session_state.route_coords = []
# if "explanation" not in st.session_state:
#     st.session_state.explanation = ""
# if "estimated_consumption" not in st.session_state:
#     st.session_state.estimated_consumption = 0
# if "consumption_unit" not in st.session_state:
#     st.session_state.consumption_unit = ""

# st.title("AutoRoute AI - Traffic Route Optimizer")

# origin = st.text_input("Origin", "Origin")
# destination = st.text_input("Destination", "Destination")
# vehicle_type = st.selectbox("Vehicle Type", ["EV", "Gasoline", "Emergency"])
# priority = st.selectbox("Priority", ["normal", "emergency", "economy"])

# def fetch_route():
#     if not origin or not destination:
#         st.error("Please enter both origin and destination.")
#         return
#     payload = {
#         "origin": origin,
#         "destination": destination,
#         "vehicle_type": vehicle_type,
#         "priority": priority,
#     }
#     try:
#         response = requests.post("http://localhost:8000/route", json=payload)
#         if response.status_code == 200:
#             data = response.json()
#             st.session_state.route_coords = data["route_coords"]
#             st.session_state.explanation = data["explanation"]
#             st.session_state.estimated_consumption = data.get("estimated_consumption", 0)
#             st.session_state.consumption_unit = data.get("consumption_unit", "")
#         else:
#             st.error(f"Error from server: {response.status_code} - {response.text}")
#     except requests.exceptions.RequestException as e:
#         st.error(f"Failed to connect to backend: {e}")

# def create_google_maps_link(coords):
#     if not coords or len(coords) < 2:
#         return ""
#     origin = f"{coords[0][0]},{coords[0][1]}"
#     destination = f"{coords[-1][0]},{coords[-1][1]}"
#     waypoints = coords[1:-1]
#     waypoints_str = "|".join([f"{p[0]},{p[1]}" for p in waypoints])
#     base_url = "https://www.google.com/maps/dir/?api=1"
#     url = f"{base_url}&origin={origin}&destination={destination}"
#     if waypoints_str:
#         url += f"&waypoints={waypoints_str}"
#     url += "&travelmode=driving"
#     return url

# if st.button("Get Route"):
#     fetch_route()

# if st.session_state.route_coords:
#     m = folium.Map(location=st.session_state.route_coords[0], zoom_start=14)

#     # Add only origin and destination markers
#     folium.Marker(st.session_state.route_coords[0], popup="Origin", icon=folium.Icon(color='green')).add_to(m)
#     folium.Marker(st.session_state.route_coords[-1], popup="Destination", icon=folium.Icon(color='red')).add_to(m)

#     # Draw full route polyline
#     folium.PolyLine(st.session_state.route_coords, color="blue", weight=5, opacity=0.7).add_to(m)

#     m.fit_bounds(st.session_state.route_coords)

#     st.subheader("Recommended Route Map")
#     st_folium(m, width=700, height=500)

#     st.subheader("Route Explanation")
#     st.write(st.session_state.explanation)

#     st.subheader("Estimated Energy/Fuel Consumption")
#     st.write(f"{st.session_state.estimated_consumption} {st.session_state.consumption_unit}")

#     maps_url = create_google_maps_link(st.session_state.route_coords)
#     if maps_url:
#         st.markdown(f"[Open route in Google Maps]({maps_url})", unsafe_allow_html=True)

import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

# Initialize session state variables
if "routes" not in st.session_state:
    st.session_state.routes = []
if "selected_route_index" not in st.session_state:
    st.session_state.selected_route_index = 0
if "explanation" not in st.session_state:
    st.session_state.explanation = ""
if "estimated_consumption" not in st.session_state:
    st.session_state.estimated_consumption = 0
if "consumption_unit" not in st.session_state:
    st.session_state.consumption_unit = ""

st.title("AutoRoute AI - Traffic Route Optimizer")

origin = st.text_input("Origin", "Origin")
destination = st.text_input("Destination", "Destination")
vehicle_type = st.selectbox("Vehicle Type", ["EV", "Gasoline", "Emergency"])
priority = st.selectbox("Priority", ["normal", "emergency", "economy"])

def fetch_routes():
    if not origin or not destination:
        st.error("Please enter both origin and destination.")
        return
    payload = {
        "origin": origin,
        "destination": destination,
        "vehicle_type": vehicle_type,
        "priority": priority,
        "alternatives": True
    }
    try:
        response = requests.post("http://localhost:8000/route", json=payload)
        if response.status_code == 200:
            data = response.json()
            st.session_state.routes = data["routes"]
            st.session_state.explanation = data["explanation"]
            st.session_state.selected_route_index = 0
            # Set energy info for first route if exists
            if len(st.session_state.routes) > 0:
                # You may want to extend backend to send consumption per route
                st.session_state.estimated_consumption = 0
                st.session_state.consumption_unit = ""
        else:
            st.error(f"Error from server: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to backend: {e}")

def create_google_maps_link(coords):
    if not coords or len(coords) < 2:
        return ""
    origin = f"{coords[0][0]},{coords[0][1]}"
    destination = f"{coords[-1][0]},{coords[-1][1]}"
    waypoints = coords[1:-1]
    waypoints_str = "|".join([f"{p[0]},{p[1]}" for p in waypoints])
    base_url = "https://www.google.com/maps/dir/?api=1"
    url = f"{base_url}&origin={origin}&destination={destination}"
    if waypoints_str:
        url += f"&waypoints={waypoints_str}"
    url += "&travelmode=driving"
    return url

if st.button("Get Routes"):
    fetch_routes()

if st.session_state.routes:
    route_descriptions = [
        f"Route {i+1}: {route['distance_km']:.2f} km, {route['duration_min']:.1f} min"
        for i, route in enumerate(st.session_state.routes)
    ]

    selected_index = st.selectbox("Select a route", range(len(route_descriptions)), format_func=lambda i: route_descriptions[i])
    st.session_state.selected_route_index = selected_index

    selected_route = st.session_state.routes[selected_index]
    route_coords = selected_route["route_coords"]

    m = folium.Map(location=route_coords[0], zoom_start=14)
    folium.Marker(route_coords[0], popup="Origin", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(route_coords[-1], popup="Destination", icon=folium.Icon(color='red')).add_to(m)
    folium.PolyLine(route_coords, color="blue", weight=5, opacity=0.7).add_to(m)
    m.fit_bounds(route_coords)

    st.subheader("Recommended Route Map")
    st_folium(m, width=700, height=500)

    st.subheader("Route Explanation")
    st.write(st.session_state.explanation)

    
    energy = selected_route.get("estimated_consumption", 0)
    unit = selected_route.get("consumption_unit", "")
    st.subheader("Estimated Energy/Fuel Consumption")
    st.write(f"{energy} {unit}")
    maps_url = create_google_maps_link(route_coords)
    if maps_url:
        st.markdown(f"[Open route in Google Maps]({maps_url})", unsafe_allow_html=True)
