
# import streamlit as st
# import requests
# import folium
# from streamlit_folium import st_folium

# # Initialize session state variables
# if "routes" not in st.session_state:
#     st.session_state.routes = []
# if "selected_route_index" not in st.session_state:
#     st.session_state.selected_route_index = 0
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

# def fetch_routes():
#     if not origin or not destination:
#         st.error("Please enter both origin and destination.")
#         return
#     payload = {
#         "origin": origin,
#         "destination": destination,
#         "vehicle_type": vehicle_type,
#         "priority": priority,
#         "alternatives": True
#     }
#     try:
#         response = requests.post("http://localhost:8000/route", json=payload)
#         if response.status_code == 200:
#             data = response.json()
#             st.session_state.routes = data["routes"]
#             st.session_state.explanation = data["explanation"]
#             st.session_state.selected_route_index = 0
#             # Set energy info for first route if exists
#             if len(st.session_state.routes) > 0:
#                 # You may want to extend backend to send consumption per route
#                 st.session_state.estimated_consumption = 0
#                 st.session_state.consumption_unit = ""
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

# if st.button("Get Routes"):
#     fetch_routes()

# if st.session_state.routes:
#     route_descriptions = [
#         f"Route {i+1}: {route['distance_km']:.2f} km, {route['duration_min']:.1f} min"
#         for i, route in enumerate(st.session_state.routes)
#     ]

#     selected_index = st.selectbox("Select a route", range(len(route_descriptions)), format_func=lambda i: route_descriptions[i])
#     st.session_state.selected_route_index = selected_index

#     selected_route = st.session_state.routes[selected_index]
#     route_coords = selected_route["route_coords"]

#     m = folium.Map(location=route_coords[0], zoom_start=14)
#     folium.Marker(route_coords[0], popup="Origin", icon=folium.Icon(color='green')).add_to(m)
#     folium.Marker(route_coords[-1], popup="Destination", icon=folium.Icon(color='red')).add_to(m)
#     folium.PolyLine(route_coords, color="blue", weight=5, opacity=0.7).add_to(m)
#     m.fit_bounds(route_coords)

#     st.subheader("Recommended Route Map")
#     st_folium(m, width=700, height=500)

#     st.subheader("Route Explanation")
#     st.write(st.session_state.explanation)

    
#     energy = selected_route.get("estimated_consumption", 0)
#     unit = selected_route.get("consumption_unit", "")
#     st.subheader("Estimated Energy/Fuel Consumption")
#     st.write(f"{energy} {unit}")
#     maps_url = create_google_maps_link(route_coords)
#     if maps_url:
#         st.markdown(f"[Open route in Google Maps]({maps_url})", unsafe_allow_html=True)

# import streamlit as st
# import requests
# import folium
# from streamlit_folium import st_folium

# # Initialize session state for routing
# if "routes" not in st.session_state:
#     st.session_state.routes = []
# if "selected_route_index" not in st.session_state:
#     st.session_state.selected_route_index = 0
# if "explanation" not in st.session_state:
#     st.session_state.explanation = ""
# if "estimated_consumption" not in st.session_state:
#     st.session_state.estimated_consumption = 0
# if "consumption_unit" not in st.session_state:
#     st.session_state.consumption_unit = ""

# # Initialize session state for chat
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# st.title("AutoRoute AI")

# # --------------------------
# # Routing UI
# # --------------------------

# st.header("Route Optimizer")

# origin = st.text_input("Origin", "Origin")
# destination = st.text_input("Destination", "Destination")
# vehicle_type = st.selectbox("Vehicle Type", ["EV", "Gasoline", "Emergency"])
# priority = st.selectbox("Priority", ["normal", "emergency", "economy"])

# def fetch_routes():
#     if not origin or not destination:
#         st.error("Please enter both origin and destination.")
#         return
#     payload = {
#         "origin": origin,
#         "destination": destination,
#         "vehicle_type": vehicle_type,
#         "priority": priority,
#         "alternatives": True
#     }
#     try:
#         response = requests.post("http://localhost:8000/route", json=payload)
#         if response.status_code == 200:
#             data = response.json()
#             st.session_state.routes = data["routes"]
#             st.session_state.explanation = data["explanation"]
#             st.session_state.selected_route_index = 0
#             if len(st.session_state.routes) > 0:
#                 first_route = st.session_state.routes[0]
#                 st.session_state.estimated_consumption = first_route.get("estimated_consumption", 0)
#                 st.session_state.consumption_unit = first_route.get("consumption_unit", "")
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

# if st.button("Get Routes"):
#     fetch_routes()

# if st.session_state.routes:
#     route_descriptions = [
#         f"Route {i+1}: {route['distance_km']:.2f} km, {route['duration_min']:.1f} min"
#         for i, route in enumerate(st.session_state.routes)
#     ]

#     selected_index = st.selectbox("Select a route", range(len(route_descriptions)), format_func=lambda i: route_descriptions[i])
#     st.session_state.selected_route_index = selected_index

#     selected_route = st.session_state.routes[selected_index]
#     route_coords = selected_route["route_coords"]

#     m = folium.Map(location=route_coords[0], zoom_start=14)
#     folium.Marker(route_coords[0], popup="Origin", icon=folium.Icon(color='green')).add_to(m)
#     folium.Marker(route_coords[-1], popup="Destination", icon=folium.Icon(color='red')).add_to(m)
#     folium.PolyLine(route_coords, color="blue", weight=5, opacity=0.7).add_to(m)
#     m.fit_bounds(route_coords)

#     st.subheader("Recommended Route Map")
#     st_folium(m, width=700, height=500)

#     st.subheader("Route Explanation")
#     st.write(st.session_state.explanation)

#     st.subheader("Estimated Energy/Fuel Consumption")
#     st.write(f"{selected_route.get('estimated_consumption', 0)} {selected_route.get('consumption_unit', '')}")

#     maps_url = create_google_maps_link(route_coords)
#     if maps_url:
#         st.markdown(f"[Open route in Google Maps]({maps_url})", unsafe_allow_html=True)

# # --------------------------
# # Chat UI
# # --------------------------

# st.header("AI Conversational Assistant")

# def send_message(message, context):
#     payload = {
#         "message": message,
#         "context": context
#     }
#     response = requests.post("http://localhost:8000/chat", json=payload)
#     if response.status_code == 200:
#         return response.json().get("reply")
#     else:
#         return "Sorry, I couldn't process your request."

# user_input = st.text_input("Ask me anything about your route or driving:")

# if st.button("Send") and user_input:
#     # Build context string from current route info
#     if st.session_state.routes and st.session_state.selected_route_index < len(st.session_state.routes):
#         sel_route = st.session_state.routes[st.session_state.selected_route_index]
#         context_text = (
#             f"Current route from {origin} to {destination}. "
#             f"Vehicle type: {vehicle_type}. "
#             f"Estimated time: {sel_route['duration_min']:.1f} minutes. "
#             f"Distance: {sel_route['distance_km']:.2f} km."
#         )
#     else:
#         context_text = ""
#     st.session_state.chat_history.append(("You", user_input))
#     bot_reply = send_message(user_input, context_text)
#     st.session_state.chat_history.append(("Assistant", bot_reply))

# for speaker, msg in st.session_state.chat_history:
#     if speaker == "You":
#         st.markdown(f"**You:** {msg}")
#     else:
#         st.markdown(f"**Assistant:** {msg}")


# import streamlit as st
# import requests
# import folium
# from streamlit_folium import st_folium

# # Initialize session state for routing
# if "routes" not in st.session_state:
#     st.session_state.routes = []
# if "selected_route_index" not in st.session_state:
#     st.session_state.selected_route_index = 0
# if "explanation" not in st.session_state:
#     st.session_state.explanation = ""
# if "estimated_consumption" not in st.session_state:
#     st.session_state.estimated_consumption = 0
# if "consumption_unit" not in st.session_state:
#     st.session_state.consumption_unit = ""

# # Initialize session state for POI search
# if "poi_results" not in st.session_state:
#     st.session_state.poi_results = []
# if "selected_poi_index" not in st.session_state:
#     st.session_state.selected_poi_index = None

# # Initialize session state for chat
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# st.title("AutoRoute AI")

# # --------------------------
# # Route Optimizer UI
# # --------------------------

# st.header("Route Optimizer")

# origin = st.text_input("Origin", "Origin")
# destination = st.text_input("Destination", "Destination")
# vehicle_type = st.selectbox("Vehicle Type", ["EV", "Gasoline", "Emergency"])
# priority = st.selectbox("Priority", ["normal", "emergency", "economy"])

# poi_query = st.text_input("Search for nearby places (e.g., coffee shop):")

# def search_poi(query, proximity):
#     if not query or proximity is None:
#         return []
#     try:
#         response = requests.post("http://localhost:8000/search_poi", json={
#             "query": query,
#             "proximity": proximity
#         })
#         if response.status_code == 200:
#             return response.json().get("results", [])
#         else:
#             st.error(f"POI search failed: {response.status_code}")
#             return []
#     except Exception as e:
#         st.error(f"Error searching POIs: {e}")
#         return []

# selected_poi = None

# def fetch_routes():
#     if not origin or not destination:
#         st.error("Please enter both origin and destination.")
#         return

#     # Get origin coords for POI proximity search
#     origin_coords = None
#     try:
#         geo_resp = requests.post("http://localhost:8000/geocode", json={"location": origin})
#         if geo_resp.status_code == 200:
#             geo_data = geo_resp.json()
#             origin_coords = geo_data.get("coordinates")
#         else:
#             st.error("Failed to geocode origin.")
#     except Exception as e:
#         st.error(f"Error geocoding origin: {e}")

#     if poi_query:
#         st.session_state.poi_results = search_poi(poi_query, origin_coords)
#         st.session_state.selected_poi_index = None

#     payload = {
#         "origin": origin,
#         "destination": destination,
#         "vehicle_type": vehicle_type,
#         "priority": priority,
#         "alternatives": True,
#     }

#     if st.session_state.selected_poi_index is not None:
#         selected = st.session_state.poi_results[st.session_state.selected_poi_index]
#         payload["detour_poi"] = selected

#     try:
#         response = requests.post("http://localhost:8000/route", json=payload)
#         if response.status_code == 200:
#             data = response.json()
#             st.session_state.routes = data["routes"]
#             st.session_state.explanation = data["explanation"]
#             st.session_state.selected_route_index = 0
#             if st.session_state.routes:
#                 first_route = st.session_state.routes[0]
#                 st.session_state.estimated_consumption = first_route.get("estimated_consumption", 0)
#                 st.session_state.consumption_unit = first_route.get("consumption_unit", "")
#         else:
#             st.error(f"Error fetching routes: {response.status_code} - {response.text}")
#     except Exception as e:
#         st.error(f"Error fetching routes: {e}")

# if st.button("Get Routes"):
#     fetch_routes()

# # Show POI search results for detour selection
# if st.session_state.poi_results:
#     poi_options = [f"{poi['name']} - {poi['address']}" for poi in st.session_state.poi_results]
#     st.session_state.selected_poi_index = st.selectbox("Select a place to detour", range(len(poi_options)), format_func=lambda i: poi_options[i])

# # Show routes and map
# if st.session_state.routes:
#     route_descriptions = [
#         f"Route {i+1}: {route['distance_km']:.2f} km, {route['duration_min']:.1f} min"
#         for i, route in enumerate(st.session_state.routes)
#     ]

#     selected_index = st.selectbox("Select a route", range(len(route_descriptions)), format_func=lambda i: route_descriptions[i])
#     st.session_state.selected_route_index = selected_index

#     selected_route = st.session_state.routes[selected_index]
#     route_coords = selected_route["route_coords"]

#     m = folium.Map(location=route_coords[0], zoom_start=14)
#     folium.Marker(route_coords[0], popup="Origin", icon=folium.Icon(color='green')).add_to(m)
#     folium.Marker(route_coords[-1], popup="Destination", icon=folium.Icon(color='red')).add_to(m)
#     folium.PolyLine(route_coords, color="blue", weight=5, opacity=0.7).add_to(m)
#     m.fit_bounds(route_coords)

#     st.subheader("Recommended Route Map")
#     st_folium(m, width=700, height=500)

#     st.subheader("Route Explanation")
#     st.write(st.session_state.explanation)

#     st.subheader("Estimated Energy/Fuel Consumption")
#     st.write(f"{selected_route.get('estimated_consumption', 0)} {selected_route.get('consumption_unit', '')}")

#     def create_google_maps_link(coords):
#         if not coords or len(coords) < 2:
#             return ""
#         origin = f"{coords[0][0]},{coords[0][1]}"
#         destination = f"{coords[-1][0]},{coords[-1][1]}"
#         waypoints = coords[1:-1]
#         waypoints_str = "|".join([f"{p[0]},{p[1]}" for p in waypoints])
#         base_url = "https://www.google.com/maps/dir/?api=1"
#         url = f"{base_url}&origin={origin}&destination={destination}"
#         if waypoints_str:
#             url += f"&waypoints={waypoints_str}"
#         url += "&travelmode=driving"
#         return url

#     maps_url = create_google_maps_link(route_coords)
#     if maps_url:
#         st.markdown(f"[Open route in Google Maps]({maps_url})", unsafe_allow_html=True)

# # --------------------------
# # Chat UI
# # --------------------------

# st.header("AI Conversational Assistant")

# def send_message(message, context):
#     payload = {"message": message, "context": context}
#     response = requests.post("http://localhost:8000/chat", json=payload)
#     if response.status_code == 200:
#         return response.json().get("reply")
#     else:
#         return "Sorry, I couldn't process your request."

# user_input = st.text_input("Ask me anything about your route or driving:")

# if st.button("Send") and user_input:
#     if st.session_state.routes and st.session_state.selected_route_index < len(st.session_state.routes):
#         sel_route = st.session_state.routes[st.session_state.selected_route_index]
#         context_text = (
#             f"Current route from {origin} to {destination}. "
#             f"Vehicle type: {vehicle_type}. "
#             f"Estimated time: {sel_route['duration_min']:.1f} minutes. "
#             f"Distance: {sel_route['distance_km']:.2f} km."
#         )
#     else:
#         context_text = ""

#     st.session_state.chat_history.append(("You", user_input))
#     bot_reply = send_message(user_input, context_text)
#     st.session_state.chat_history.append(("Assistant", bot_reply))

# for speaker, msg in st.session_state.chat_history:
#     if speaker == "You":
#         st.markdown(f"**You:** {msg}")
#     else:
#         st.markdown(f"**Assistant:** {msg}")


import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

# Initialize session state for routing
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

# Initialize session state for POI search
if "poi_results" not in st.session_state:
    st.session_state.poi_results = []
if "selected_poi_index" not in st.session_state:
    st.session_state.selected_poi_index = None

# Initialize session state for chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("AutoRoute AI")

# Route optimizer UI
st.header("Route Optimizer")

origin = st.text_input("Origin", "Origin")
destination = st.text_input("Destination", "Destination")
vehicle_type = st.selectbox("Vehicle Type", ["EV", "Gasoline", "Emergency"])
priority = st.selectbox("Priority", ["normal", "emergency", "economy"])

poi_query = st.text_input("Search for nearby places (e.g., coffee shop):")

def search_poi(query, proximity):
    if not query or proximity is None:
        return []
    try:
        response = requests.post("http://localhost:8000/search_poi", json={
            "query": query,
            "proximity": proximity
        })
        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            st.error(f"POI search failed: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error searching POIs: {e}")
        return []

selected_poi = None

def fetch_routes():
    if not origin or not destination:
        st.error("Please enter both origin and destination.")
        return

    # Get origin coords for POI proximity search
    origin_coords = None
    try:
        geo_resp = requests.post("http://localhost:8000/geocode", json={"location": origin})
        if geo_resp.status_code == 200:
            geo_data = geo_resp.json()
            origin_coords = geo_data.get("coordinates")
        else:
            st.error("Failed to geocode origin.")
    except Exception as e:
        st.error(f"Error geocoding origin: {e}")

    if poi_query:
        st.session_state.poi_results = search_poi(poi_query, origin_coords)
        st.session_state.selected_poi_index = None

    payload = {
        "origin": origin,
        "destination": destination,
        "vehicle_type": vehicle_type,
        "priority": priority,
        "alternatives": True,
    }

    if st.session_state.selected_poi_index is not None:
        selected = st.session_state.poi_results[st.session_state.selected_poi_index]
        payload["detour_poi"] = selected

    try:
        response = requests.post("http://localhost:8000/route", json=payload)
        if response.status_code == 200:
            data = response.json()
            st.session_state.routes = data["routes"]
            st.session_state.explanation = data["explanation"]
            st.session_state.selected_route_index = 0
            if st.session_state.routes:
                first_route = st.session_state.routes[0]
                st.session_state.estimated_consumption = first_route.get("estimated_consumption", 0)
                st.session_state.consumption_unit = first_route.get("consumption_unit", "")
        else:
            st.error(f"Error fetching routes: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Error fetching routes: {e}")

if st.button("Get Routes"):
    fetch_routes()

# Show POI search results for detour selection
if st.session_state.poi_results:
    poi_options = [f"{poi['name']} - {poi['address']}" for poi in st.session_state.poi_results]
    st.session_state.selected_poi_index = st.selectbox("Select a place to detour", range(len(poi_options)), format_func=lambda i: poi_options[i])

# Show routes and map
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

    st.subheader("Estimated Energy/Fuel Consumption")
    st.write(f"{selected_route.get('estimated_consumption', 0)} {selected_route.get('consumption_unit', '')}")

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

    maps_url = create_google_maps_link(route_coords)
    if maps_url:
        st.markdown(f"[Open route in Google Maps]({maps_url})", unsafe_allow_html=True)

# Chat UI

st.header("AI Conversational Assistant")

def send_message(message, context):
    payload = {"message": message, "context": context}
    response = requests.post("http://localhost:8000/chat", json=payload)
    if response.status_code == 200:
        return response.json().get("reply")
    else:
        return "Sorry, I couldn't process your request."

user_input = st.text_input("Ask me anything about your route or driving:")

if st.button("Send") and user_input:
    if st.session_state.routes and st.session_state.selected_route_index < len(st.session_state.routes):
        sel_route = st.session_state.routes[st.session_state.selected_route_index]
        context_text = (
            f"Current route from {origin} to {destination}. "
            f"Vehicle type: {vehicle_type}. "
            f"Estimated time: {sel_route['duration_min']:.1f} minutes. "
            f"Distance: {sel_route['distance_km']:.2f} km."
        )
        if sel_route.get("detour_poi"):
            dp = sel_route["detour_poi"]
            context_text += f" Detour at {dp.get('name')} located at {dp.get('address')}."
    else:
        context_text = ""

    st.session_state.chat_history.append(("You", user_input))
    bot_reply = send_message(user_input, context_text)
    st.session_state.chat_history.append(("Assistant", bot_reply))

for speaker, msg in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**Assistant:** {msg}")
