def estimate_energy_consumption(distance_km, duration_min, stops=0, elevation_gain_m=0, vehicle_type="EV"):
    """
    Simplified energy/fuel consumption estimate.
    duration_min used to calculate average speed.
    """
    avg_speed_kmph = (distance_km / (duration_min / 60)) if duration_min > 0 else 30  # fallback 30 km/h

    if vehicle_type == "EV":
        base_consumption = 0.18  # kWh per km average
        stop_penalty = stops * 0.01
        elevation_penalty = elevation_gain_m * 0.005
        total_consumption = distance_km * base_consumption + stop_penalty + elevation_penalty
        return round(total_consumption, 2), "kWh"
    else:
        base_consumption = 0.08  # liters per km average
        stop_penalty = stops * 0.005
        elevation_penalty = elevation_gain_m * 0.002
        total_consumption = distance_km * base_consumption + stop_penalty + elevation_penalty
        return round(total_consumption, 2), "liters"
from typing import List

def get_bbox(route_coords: List[List[float]]) -> List[float]:
    lats = [pt[0] for pt in route_coords]
    lons = [pt[1] for pt in route_coords]
    return [min(lons), min(lats), max(lons), max(lats)]