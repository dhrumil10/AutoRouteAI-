

# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import List
# import os
# import sys
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# from agents.routing_agent import RoutingAgent
# from agents.assistant_agent import AssistantAgent

# app = FastAPI(title="AutoRoute AI Backend")

# # Load ORS API key from env
# ORS_API_KEY = os.getenv("ORS_API_KEY")
# routing_agent = RoutingAgent(ORS_API_KEY)
# assistant_agent = AssistantAgent()

# # Example: Simple geocoding map for testing (replace with real geocoding)
# named_locations = {
#     "Origin": (42.3601, -71.0589),
#     "Destination": (42.3650, -71.0530),
#     "Main St": (42.3615, -71.0570),
#     "2nd Ave": (42.3625, -71.0540),
#     "3rd Blvd": (42.3635, -71.0550),
# }

# class RouteRequest(BaseModel):
#     origin: str
#     destination: str
#     vehicle_type: str = "EV"
#     priority: str = "normal"

# class RouteResponse(BaseModel):
#     route_coords: List[List[float]]  # [[lat, lon], ...]
#     explanation: str
#     distance_km: float
#     duration_min: float

# @app.post("/route", response_model=RouteResponse)
# async def compute_route(request: RouteRequest):
#     origin_coord = named_locations.get(request.origin)
#     destination_coord = named_locations.get(request.destination)
#     if not origin_coord or not destination_coord:
#         return {"route_coords": [], "explanation": "Invalid origin or destination", "distance_km": 0, "duration_min": 0}

#     route_data = routing_agent.compute_route(origin_coord, destination_coord)

#     explanation = assistant_agent.generate_explanation(
#         route=["Origin", "Destination"],  # You can customize this with better logic
#         traffic_data={},                  # You can add traffic data if available
#     ) + f"\n\nDistance: {route_data['distance_km']:.2f} km, Estimated time: {route_data['duration_min']:.1f} minutes."

#     return RouteResponse(
#         route_coords=route_data['route_coords'],
#         explanation=explanation,
#         distance_km=route_data['distance_km'],
#         duration_min=route_data['duration_min']
#     )


import os
from fastapi import FastAPI
from pydantic import BaseModel
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from typing import List
from agents.routing_agent import RoutingAgent
from agents.assistant_agent import AssistantAgent


app = FastAPI(title="AutoRoute AI Backend")

MAPBOX_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN")
routing_agent = RoutingAgent(MAPBOX_TOKEN)
assistant_agent = AssistantAgent()

named_locations = {
    "Origin": (42.3601, -71.0589),
    "Destination": (42.3650, -71.0530),
    # Add more as needed
}

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

@app.post("/route", response_model=RouteResponse)
async def compute_route(request: RouteRequest):
    origin_coord = named_locations.get(request.origin)
    destination_coord = named_locations.get(request.destination)

    if not origin_coord or not destination_coord:
        return {
            "route_coords": [],
            "explanation": "Invalid origin or destination",
            "distance_km": 0,
            "duration_min": 0,
        }

    route_data = routing_agent.compute_route(
        origin_coord, destination_coord, priority=request.priority
    )

    explanation = assistant_agent.generate_explanation(
        route=[request.origin, request.destination],
        traffic_data={},
    ) + f"\n\nDistance: {route_data['distance_km']:.2f} km, Estimated time: {route_data['duration_min']:.1f} minutes."

    if request.priority == "economy":
        explanation += "\n\nThis route is optimized for fuel economy by avoiding highways and toll roads."

    return RouteResponse(
        route_coords=route_data["route_coords"],
        explanation=explanation,
        distance_km=route_data["distance_km"],
        duration_min=route_data["duration_min"],
    )
