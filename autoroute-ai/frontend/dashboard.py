# import streamlit as st
# import requests

# st.title("AutoRoute AI - Traffic Route Optimizer")

# origin = st.text_input("Origin", "Main St")
# destination = st.text_input("Destination", "3rd Blvd")
# vehicle_type = st.selectbox("Vehicle Type", ["EV", "Gasoline", "Emergency"])
# priority = st.selectbox("Priority", ["normal", "emergency"])

# if st.button("Get Route"):
#     if not origin or not destination:
#         st.error("Please enter both origin and destination.")
#     else:
#         payload = {
#             "origin": origin,
#             "destination": destination,
#             "vehicle_type": vehicle_type,
#             "priority": priority,
#         }
#         try:
#             response = requests.post("http://localhost:8000/route", json=payload)
#             if response.status_code == 200:
#                 data = response.json()
#                 st.subheader("Recommended Route")
#                 st.write(" → ".join(data["route"]))
#                 st.subheader("Route Explanation")
#                 st.write(data["explanation"])
#             else:
#                 st.error(f"Error from server: {response.status_code} - {response.text}")
#         except requests.exceptions.RequestException as e:
#             st.error(f"Failed to connect to backend: {e}")



# import streamlit as st
# import requests
# import folium
# from streamlit_folium import st_folium

# # Sample coordinates for roads (replace with your real coords)
# road_coords = {
#     "Origin": (42.3601, -71.0589),
#     "Main St": (42.3615, -71.0570),
#     "2nd Ave": (42.3625, -71.0540),
#     "3rd Blvd": (42.3635, -71.0550),
#     "Destination": (42.3650, -71.0530)
# }

# # Initialize session state variables if not already set
# if "route" not in st.session_state:
#     st.session_state.route = []
# if "explanation" not in st.session_state:
#     st.session_state.explanation = ""

# st.title("AutoRoute AI - Traffic Route Optimizer")

# origin = st.text_input("Origin", "Origin")
# destination = st.text_input("Destination", "Destination")
# vehicle_type = st.selectbox("Vehicle Type", ["EV", "Gasoline", "Emergency"])
# priority = st.selectbox("Priority", ["normal", "emergency"])

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
#             st.session_state.route = data["route"]
#             st.session_state.explanation = data["explanation"]
#         else:
#             st.error(f"Error from server: {response.status_code} - {response.text}")
#     except requests.exceptions.RequestException as e:
#         st.error(f"Failed to connect to backend: {e}")

# if st.button("Get Route"):
#     fetch_route()

# if st.session_state.route:
#     # Create folium map centered on first point
#     first_point = st.session_state.route[0]
#     center_coords = road_coords.get(first_point, (42.3601, -71.0589))
#     m = folium.Map(location=center_coords, zoom_start=14)

#     # Add markers and polyline for the route
#     route_coords = []
#     for road in st.session_state.route:
#         coords = road_coords.get(road)
#         if coords:
#             folium.Marker(coords, popup=road).add_to(m)
#             route_coords.append(coords)

#     if len(route_coords) > 1:
#         folium.PolyLine(route_coords, color="blue", weight=5, opacity=0.7).add_to(m)

#     st.subheader("Recommended Route Map")
#     st_data = st_folium(m, width=700, height=500)

#     st.subheader("Route Explanation")
#     st.write(st.session_state.explanation)


# import streamlit as st
# import requests
# import folium
# from folium import Icon
# from streamlit_folium import st_folium
# import urllib.parse

# # Sample coordinates for roads (replace with your real coords)
# road_coords = {
#     "Origin": (42.3601, -71.0589),
#     "Main St": (42.3615, -71.0570),
#     "2nd Ave": (42.3625, -71.0540),
#     "3rd Blvd": (42.3635, -71.0550),
#     "Destination": (42.3650, -71.0530)
# }

# if "route" not in st.session_state:
#     st.session_state.route = []
# if "explanation" not in st.session_state:
#     st.session_state.explanation = ""

# st.title("AutoRoute AI - Traffic Route Optimizer")

# origin = st.text_input("Origin", "Origin")
# destination = st.text_input("Destination", "Destination")
# vehicle_type = st.selectbox("Vehicle Type", ["EV", "Gasoline", "Emergency"])
# priority = st.selectbox("Priority", ["normal", "emergency"])

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
#             st.session_state.route = data["route"]
#             st.session_state.explanation = data["explanation"]
#         else:
#             st.error(f"Error from server: {response.status_code} - {response.text}")
#     except requests.exceptions.RequestException as e:
#         st.error(f"Failed to connect to backend: {e}")

# def create_google_maps_link(route: list) -> str:
#     if len(route) < 2:
#         return ""

#     origin = urllib.parse.quote(route[0])
#     destination = urllib.parse.quote(route[-1])
#     waypoints = route[1:-1]
#     waypoints_encoded = "|".join([urllib.parse.quote(wp) for wp in waypoints])

#     base_url = "https://www.google.com/maps/dir/?api=1"
#     url = f"{base_url}&origin={origin}&destination={destination}"
#     if waypoints_encoded:
#         url += f"&waypoints={waypoints_encoded}"
#     url += "&travelmode=driving"
#     return url

# if st.button("Get Route"):
#     fetch_route()

# if st.session_state.route:
#     m = folium.Map(location=[42.3601, -71.0589], zoom_start=13)

#     route_coords = []
#     for i, road in enumerate(st.session_state.route):
#         coords = road_coords.get(road)
#         if coords:
#             if i == 0:
#                 color = 'green'
#             elif i == len(st.session_state.route) - 1:
#                 color = 'red'
#             else:
#                 color = 'blue'
#             folium.Marker(coords, popup=road, icon=Icon(color=color)).add_to(m)
#             route_coords.append(coords)

#     if len(route_coords) > 1:
#         folium.PolyLine(route_coords, color="blue", weight=5, opacity=0.7).add_to(m)

#     m.fit_bounds(route_coords)

#     st.subheader("Recommended Route Map")
#     st_folium(m, width=700, height=500)

#     st.subheader("Route Explanation")
#     st.write(st.session_state.explanation)

#     maps_url = create_google_maps_link(st.session_state.route)
#     if maps_url:
#         st.markdown(f"[Open route in Google Maps]({maps_url})", unsafe_allow_html=True)



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
# priority = st.selectbox("Priority", ["normal", "emergency"])

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

#     maps_url = create_google_maps_link(st.session_state.route_coords)
#     if maps_url:
#         st.markdown(f"[Open route in Google Maps]({maps_url})", unsafe_allow_html=True)



import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import urllib.parse

if "route_coords" not in st.session_state:
    st.session_state.route_coords = []
if "explanation" not in st.session_state:
    st.session_state.explanation = ""

st.title("AutoRoute AI - Traffic Route Optimizer")

origin = st.text_input("Origin", "Origin")
destination = st.text_input("Destination", "Destination")
vehicle_type = st.selectbox("Vehicle Type", ["EV", "Gasoline", "Emergency"])
# priority = st.selectbox("Priority", ["normal", "emergency"])
priority = st.selectbox("Priority", ["normal", "emergency", "economy"])

def fetch_route():
    if not origin or not destination:
        st.error("Please enter both origin and destination.")
        return
    payload = {
        "origin": origin,
        "destination": destination,
        "vehicle_type": vehicle_type,
        "priority": priority,
    }
    try:
        response = requests.post("http://localhost:8000/route", json=payload)
        if response.status_code == 200:
            data = response.json()
            st.session_state.route_coords = data["route_coords"]
            st.session_state.explanation = data["explanation"]
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

if st.button("Get Route"):
    fetch_route()

if st.session_state.route_coords:
    # Center map on first coord
    m = folium.Map(location=st.session_state.route_coords[0], zoom_start=14)

    # Add start and end markers
    folium.Marker(st.session_state.route_coords[0], popup="Origin", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(st.session_state.route_coords[-1], popup="Destination", icon=folium.Icon(color='red')).add_to(m)

    # Draw route polyline
    folium.PolyLine(st.session_state.route_coords, color="blue", weight=5, opacity=0.7).add_to(m)

    m.fit_bounds(st.session_state.route_coords)

    st.subheader("Recommended Route Map")
    st_folium(m, width=700, height=500)

    st.subheader("Route Explanation")
    st.write(st.session_state.explanation)

    maps_url = create_google_maps_link(st.session_state.route_coords)
    if maps_url:
        st.markdown(f"[Open route in Google Maps]({maps_url})", unsafe_allow_html=True)
