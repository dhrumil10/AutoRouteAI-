import requests

class GeoCoder:
    def __init__(self, mapbox_token: str):
        self.token = mapbox_token
        self.base_url = "https://api.mapbox.com/geocoding/v5/mapbox.places"

    def geocode(self, location: str):
        url = f"{self.base_url}/{location}.json"
        params = {
            "access_token": self.token,
            "limit": 1
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        features = data.get("features")
        if features:
            coords = features[0]["center"]  # [lon, lat]
            return coords[1], coords[0]     # (lat, lon)
        else:
            return None
