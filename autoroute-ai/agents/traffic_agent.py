import requests

class TrafficAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"

    def get_traffic_flow(self, lat: float, lon: float):
        """
        Fetch traffic flow data for a specific location.
        Returns dict with traffic info or None.
        """
        params = {
            "point": f"{lat},{lon}",
            "unit": "KMPH",
            "openLr": False,
            "key": self.api_key
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            flow = data.get("flowSegmentData", {})
            return {
                "currentSpeed": flow.get("currentSpeed"),
                "freeFlowSpeed": flow.get("freeFlowSpeed"),
                "confidence": flow.get("confidence"),
                "jamFactor": flow.get("jamFactor"),
                "roadClosure": flow.get("roadClosure"),
                "roadName": flow.get("roadName"),
            }
        except Exception as e:
            print(f"Error fetching traffic flow: {e}")
            return None
