import json
from typing import Dict, Any

class SensorAgent:
    def __init__(self, traffic_data_path: str):
        self.traffic_data_path = traffic_data_path
        self.traffic_data = {}

    def load_traffic_data(self) -> Dict[str, Any]:
        """Load traffic data from JSON file or API"""
        try:
            with open(self.traffic_data_path, 'r') as f:
                self.traffic_data = json.load(f)
            return self.traffic_data
        except Exception as e:
            print(f"Error loading traffic data: {e}")
            return {}

    def get_congestion_level(self, location: str) -> str:
        """Return congestion level for a given location"""
        if not self.traffic_data:
            self.load_traffic_data()
        return self.traffic_data.get(location, {}).get("congestion", "unknown")

# Example usage:
if __name__ == "__main__":
    sensor = SensorAgent(traffic_data_path="../data/simulated_traffic.json")
    data = sensor.load_traffic_data()
    print("Loaded traffic data:", data)
    congestion = sensor.get_congestion_level("Main St")
    print(f"Congestion on Main St: {congestion}")
