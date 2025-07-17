import requests

class POIAgent:
    def __init__(self, mapbox_token: str):
        self.token = mapbox_token
        self.base_url = "https://api.mapbox.com/geocoding/v5/mapbox.places"

    def search_poi(self, query: str, proximity: tuple, limit: int = 5):
        url = f"{self.base_url}/{query}.json"
        params = {
            "access_token": self.token,
            "proximity": f"{proximity[1]},{proximity[0]}",  # lon,lat
            "limit": limit,
            "types": "poi"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        results = []
        for feature in data.get("features", []):
            results.append({
                "name": feature.get("text"),
                "address": feature.get("place_name"),
                "coordinates": feature.get("center")[::-1],  # lat, lon
            })
        return results
