import requests
from typing import List, Dict, Optional

class IncidentAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.tomtom.com/traffic/services/5/incidentDetails"

    def fetch_incidents(self, bbox: List[float]) -> Optional[List[Dict]]:
        """
        Fetch traffic incidents within a bounding box.
        bbox: [minLon, minLat, maxLon, maxLat]
        Returns list of incidents or None on failure.
        """
        params = {
            "bbox": ",".join(map(str, bbox)),
            "key": self.api_key,
            "language": "en-US",
            "format": "json"
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            incidents = data.get("incidents", [])
            return incidents
        except Exception as e:
            print(f"Error fetching incidents: {e}")
            return None

    def filter_route_incidents(self, incidents: List[Dict], route_coords: List[List[float]], threshold_meters: float = 500) -> List[Dict]:
        """
        Filter incidents close to the route polyline within threshold meters.
        For simplicity, this example checks incident location distance from route points.
        """
        from geopy.distance import geodesic

        filtered = []
        for incident in incidents:
            incident_lat = incident.get("point", {}).get("latitude")
            incident_lon = incident.get("point", {}).get("longitude")
            if incident_lat is None or incident_lon is None:
                continue
            incident_point = (incident_lat, incident_lon)

            # Check distance to any route point
            for coord in route_coords:
                route_point = (coord[0], coord[1])
                dist = geodesic(incident_point, route_point).meters
                if dist <= threshold_meters:
                    filtered.append(incident)
                    break
        return filtered
