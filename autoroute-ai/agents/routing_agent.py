
# import openrouteservice
# from openrouteservice import convert

# class RoutingAgent:
#     def __init__(self, ors_api_key: str):
#         self.client = openrouteservice.Client(key=ors_api_key)

#     def compute_route(self, origin_coord, destination_coord, priority="normal"):
#         """
#         origin_coord, destination_coord: (lat, lon)
#         priority: "normal" or "economy"
#         """
#         coords = [
#             (origin_coord[1], origin_coord[0]),  # ORS expects (lon, lat)
#             (destination_coord[1], destination_coord[0])
#         ]

#         params = {
#             "coordinates": coords,
#             "profile": "driving-car",
#             "format_out": "geojson",
#             "instructions": True,
#         }

#         # For economy, avoid highways and tolls to encourage smooth, fuel-saving routes
#         if priority == "economy":
#             params["options"] = {
#                 "avoid_features": ["highways", "tollways"]
#             }

#         routes = self.client.directions(**params)

#         geometry = routes['routes'][0]['geometry']
#         decoded = convert.decode_polyline(geometry)
#         coords_list = [[lat, lon] for lon, lat in decoded['coordinates']]

#         summary = routes['routes'][0]['summary']
#         distance_km = summary['distance'] / 1000
#         duration_min = summary['duration'] / 60

#         return {
#             'route_coords': coords_list,
#             'distance_km': distance_km,
#             'duration_min': duration_min
#         }

import os
import requests

class RoutingAgent:
    def __init__(self, mapbox_token: str):
        self.token = mapbox_token
        self.base_url = "https://api.mapbox.com/directions/v5/mapbox/driving"

    def compute_route(self, origin_coord, destination_coord, priority="normal"):
        """
        origin_coord, destination_coord: (lat, lon)
        priority: "normal" or "economy"
        """
        coords = f"{origin_coord[1]},{origin_coord[0]};{destination_coord[1]},{destination_coord[0]}"  # lon,lat

        params = {
            "access_token": self.token,
            "geometries": "geojson",
            "overview": "full"
        }

        if priority == "economy":
            params["exclude"] = "motorway,toll"  # avoid highways and tolls for economy routing

        response = requests.get(f"{self.base_url}/{coords}", params=params)
        response.raise_for_status()

        data = response.json()
        if "routes" not in data or len(data["routes"]) == 0:
            raise ValueError("No routes found")

        route = data["routes"][0]
        coords_list = route["geometry"]["coordinates"]  # list of [lon, lat]

        # Convert to [lat, lon] for folium
        route_latlon = [[lat, lon] for lon, lat in coords_list]

        distance_km = route["distance"] / 1000
        duration_min = route["duration"] / 60

        return {
            "route_coords": route_latlon,
            "distance_km": distance_km,
            "duration_min": duration_min
        }
