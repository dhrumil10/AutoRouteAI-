
# import os
# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import List
# import sys
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# from agents.routing_agent import RoutingAgent
# from agents.assistant_agent import AssistantAgent
# from agents.geocoder import GeoCoder
# from agents.traffic_agent import TrafficAgent

# app = FastAPI(title="AutoRoute AI Backend")

# MAPBOX_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN")
# TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")

# routing_agent = RoutingAgent(MAPBOX_TOKEN)
# geo_coder = GeoCoder(MAPBOX_TOKEN)
# assistant_agent = AssistantAgent()
# traffic_agent = TrafficAgent(TOMTOM_API_KEY)

# class RouteRequest(BaseModel):
#     origin: str
#     destination: str
#     vehicle_type: str = "EV"
#     priority: str = "normal"

# class RouteResponse(BaseModel):
#     route_coords: List[List[float]]
#     explanation: str
#     distance_km: float
#     duration_min: float

# @app.post("/route", response_model=RouteResponse)
# async def compute_route(request: RouteRequest):
#     origin_coord = geo_coder.geocode(request.origin)
#     destination_coord = geo_coder.geocode(request.destination)

#     if not origin_coord or not destination_coord:
#         return {
#             "route_coords": [],
#             "explanation": "Could not find location coordinates for origin or destination.",
#             "distance_km": 0,
#             "duration_min": 0,
#         }

#     route_data = routing_agent.compute_route(origin_coord, destination_coord, priority=request.priority)

#     # Fetch traffic data for origin and destination points (sample)
#     origin_traffic = traffic_agent.get_traffic_flow(*origin_coord)
#     dest_traffic = traffic_agent.get_traffic_flow(*destination_coord)

#     traffic_info = ""
#     if origin_traffic:
#         traffic_info += f"Origin traffic speed: {origin_traffic['currentSpeed']} KMPH. "
#     if dest_traffic:
#         traffic_info += f"Destination traffic speed: {dest_traffic['currentSpeed']} KMPH."

#     explanation = assistant_agent.generate_explanation(
#         route=[request.origin, request.destination],
#         traffic_data={
#             "origin": origin_traffic,
#             "destination": dest_traffic
#         },
#     ) + f"\n\nDistance: {route_data['distance_km']:.2f} km, Estimated time: {route_data['duration_min']:.1f} minutes.\n{traffic_info}"

#     if request.priority == "economy":
#         explanation += "\n\nThis route is optimized for fuel economy by avoiding highways and toll roads."

#     return RouteResponse(
#         route_coords=route_data["route_coords"],
#         explanation=explanation,
#         distance_km=route_data["distance_km"],
#         duration_min=route_data["duration_min"],
#     )

import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from agents.routing_agent import RoutingAgent
from agents.assistant_agent import AssistantAgent
from agents.geocoder import GeoCoder
from agents.traffic_agent import TrafficAgent
from agents.utils import estimate_energy_consumption

app = FastAPI(title="AutoRoute AI Backend")

MAPBOX_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN")
TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")

routing_agent = RoutingAgent(MAPBOX_TOKEN)
geo_coder = GeoCoder(MAPBOX_TOKEN)
assistant_agent = AssistantAgent()
traffic_agent = TrafficAgent(TOMTOM_API_KEY)

class RouteRequest(BaseModel):
    origin: str
    destination: str
    vehicle_type: str = "EV"
    priority: str = "normal"

class RouteResponse(BaseModel):
    route_coords: List[List[float]]
    explanation: str
    distance_km: float
    duration_min: float
    estimated_consumption: float
    consumption_unit: str

@app.post("/route", response_model=RouteResponse)
async def compute_route(request: RouteRequest):
    origin_coord = geo_coder.geocode(request.origin)
    destination_coord = geo_coder.geocode(request.destination)

    if not origin_coord or not destination_coord:
        return {
            "route_coords": [],
            "explanation": "Could not find location coordinates for origin or destination.",
            "distance_km": 0,
            "duration_min": 0,
            "estimated_consumption": 0,
            "consumption_unit": "",
        }

    route_data = routing_agent.compute_route(origin_coord, destination_coord, priority=request.priority)

    # For simplicity, assume stops=0 and elevation_gain=0 now
    energy_estimate, energy_unit = estimate_energy_consumption(
        route_data["distance_km"],
        route_data["duration_min"],
        stops=0,
        elevation_gain_m=0,
        vehicle_type=request.vehicle_type,
    )

    explanation = assistant_agent.generate_explanation(
        route=[request.origin, request.destination],
        traffic_data={},
        energy_estimate=energy_estimate,
        energy_unit=energy_unit,
        vehicle_type=request.vehicle_type,
    ) + f"\n\nDistance: {route_data['distance_km']:.2f} km, Estimated time: {route_data['duration_min']:.1f} minutes."

    if request.priority == "economy":
        explanation += "\n\nThis route is optimized for fuel economy by avoiding highways and toll roads."

    return RouteResponse(
        route_coords=route_data["route_coords"],
        explanation=explanation,
        distance_km=route_data["distance_km"],
        duration_min=route_data["duration_min"],
        estimated_consumption=energy_estimate,
        consumption_unit=energy_unit,
    )
