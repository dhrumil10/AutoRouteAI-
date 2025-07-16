
# import os
# import requests

# class RoutingAgent:
#     def __init__(self, mapbox_token: str):
#         self.token = mapbox_token
#         self.base_url = "https://api.mapbox.com/directions/v5/mapbox/driving"

#     def compute_route(self, origin_coord, destination_coord, priority="normal"):
#         """
#         origin_coord, destination_coord: (lat, lon)
#         priority: "normal" or "economy"
#         """
#         coords = f"{origin_coord[1]},{origin_coord[0]};{destination_coord[1]},{destination_coord[0]}"  # lon,lat

#         params = {
#             "access_token": self.token,
#             "geometries": "geojson",
#             "overview": "full"
#         }

#         if priority == "economy":
#             params["exclude"] = "motorway,toll"  # avoid highways and tolls for economy routing

#         response = requests.get(f"{self.base_url}/{coords}", params=params)
#         response.raise_for_status()

#         data = response.json()
#         if "routes" not in data or len(data["routes"]) == 0:
#             raise ValueError("No routes found")

#         route = data["routes"][0]
#         coords_list = route["geometry"]["coordinates"]  # list of [lon, lat]

#         # Convert to [lat, lon] for folium
#         route_latlon = [[lat, lon] for lon, lat in coords_list]

#         distance_km = route["distance"] / 1000
#         duration_min = route["duration"] / 60

#         return {
#             "route_coords": route_latlon,
#             "distance_km": distance_km,
#             "duration_min": duration_min
#         }

import os
import requests

class RoutingAgent:
    def __init__(self, mapbox_token: str):
        self.token = mapbox_token
        self.base_url = "https://api.mapbox.com/directions/v5/mapbox/driving"

    def compute_route(self, origin_coord, destination_coord, priority="normal"):
        coords = f"{origin_coord[1]},{origin_coord[0]};{destination_coord[1]},{destination_coord[0]}"  # lon,lat

        params = {
            "access_token": self.token,
            "geometries": "geojson",
            "overview": "full"
        }

        if priority == "economy":
            params["exclude"] = "motorway,toll"

        response = requests.get(f"{self.base_url}/{coords}", params=params)
        response.raise_for_status()

        data = response.json()
        if "routes" not in data or len(data["routes"]) == 0:
            raise ValueError("No routes found")

        route = data["routes"][0]
        coords_list = route["geometry"]["coordinates"]

        # Convert to [lat, lon] for folium
        route_latlon = [[lat, lon] for lon, lat in coords_list]

        distance_km = route["distance"] / 1000
        duration_min = route["duration"] / 60

        return {
            "route_coords": route_latlon,
            "distance_km": distance_km,
            "duration_min": duration_min
        }
