

# import os
# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import List
# from fastapi import Request
# import sys
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# from agents.ConversationAgent import ConversationAgent
# from agents.routing_agent import RoutingAgent
# from agents.assistant_agent import AssistantAgent
# from agents.geocoder import GeoCoder
# from agents.incident_agent import IncidentAgent
# from agents.utils import estimate_energy_consumption, get_bbox

# app = FastAPI(title="AutoRoute AI Backend")

# MAPBOX_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN")
# TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")

# routing_agent = RoutingAgent(MAPBOX_TOKEN)
# geo_coder = GeoCoder(MAPBOX_TOKEN)
# assistant_agent = AssistantAgent()
# incident_agent = IncidentAgent(TOMTOM_API_KEY)

# class SingleRoute(BaseModel):
#     route_coords: List[List[float]]
#     distance_km: float
#     duration_min: float
#     estimated_consumption: float
#     consumption_unit: str

# class RouteRequest(BaseModel):
#     origin: str
#     destination: str
#     vehicle_type: str = "EV"
#     priority: str = "normal"
#     alternatives: bool = True

# class RouteResponse(BaseModel):
#     routes: List[SingleRoute]
#     explanation: str

# @app.post("/route", response_model=RouteResponse)
# async def compute_route(request: RouteRequest):
#     origin_coord = geo_coder.geocode(request.origin)
#     destination_coord = geo_coder.geocode(request.destination)

#     if not origin_coord or not destination_coord:
#         return {
#             "routes": [],
#             "explanation": "Could not find location coordinates for origin or destination."
#         }

#     raw_routes = routing_agent.compute_routes(
#         origin_coord,
#         destination_coord,
#         priority=request.priority,
#         alternatives=request.alternatives
#     )

#     routes = []
#     for route in raw_routes:
#         energy, unit = estimate_energy_consumption(
#             route['distance_km'],
#             route['duration_min'],
#             stops=0,
#             elevation_gain_m=0,
#             vehicle_type=request.vehicle_type
#         )
#         route['estimated_consumption'] = energy
#         route['consumption_unit'] = unit
#         routes.append(route)

#     # Use first route for incident analysis and explanation
#     primary_route = routes[0] if routes else None

#     incident_summary = ""
#     if primary_route:
#         bbox = get_bbox(primary_route["route_coords"])
#         incidents = incident_agent.fetch_incidents(bbox)
#         relevant_incidents = incident_agent.filter_route_incidents(incidents or [], primary_route["route_coords"])

#         if relevant_incidents:
#             incident_summary = (
#                 f"{len(relevant_incidents)} incident(s) detected on your route: "
#                 + ", ".join([inc.get("type", "Unknown") for inc in relevant_incidents])
#                 + ". You may experience delays."
#             )

#     explanation = assistant_agent.generate_explanation(
#         route=[request.origin, request.destination],
#         traffic_data={},
#         energy_estimate=primary_route['estimated_consumption'] if primary_route else 0,
#         energy_unit=primary_route['consumption_unit'] if primary_route else "",
#         vehicle_type=request.vehicle_type,
#     ) + f"\n\n{incident_summary}\nNumber of route alternatives: {len(routes)}"

#     return RouteResponse(routes=routes, explanation=explanation)


    
# conversation_agent = ConversationAgent()

# @app.post("/chat")
# async def chat_endpoint(request: Request):
#     data = await request.json()
#     user_message = data.get("message")
#     context = data.get("context", "")

#     if not user_message:
#         return {"error": "No message provided"}

#     conversation_agent.add_system_message(context)
#     conversation_agent.add_user_message(user_message)
#     reply = conversation_agent.generate_response()
#     return {"reply": reply}




# import os
# from fastapi import FastAPI, Request
# from pydantic import BaseModel
# from typing import List, Optional
# import sys
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# from agents.routing_agent import RoutingAgent
# from agents.assistant_agent import AssistantAgent
# from agents.geocoder import GeoCoder
# from agents.poi_agent import POIAgent
# from agents.utils import estimate_energy_consumption

# app = FastAPI(title="AutoRoute AI Backend")

# MAPBOX_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN")
# TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")

# routing_agent = RoutingAgent(MAPBOX_TOKEN)
# geo_coder = GeoCoder(MAPBOX_TOKEN)
# assistant_agent = AssistantAgent()
# poi_agent = POIAgent(MAPBOX_TOKEN)

# class SingleRoute(BaseModel):
#     route_coords: List[List[float]]
#     distance_km: float
#     duration_min: float
#     estimated_consumption: float
#     consumption_unit: str

# class RouteRequest(BaseModel):
#     origin: str
#     destination: str
#     vehicle_type: str = "EV"
#     priority: str = "normal"
#     alternatives: bool = True
#     detour_poi: Optional[dict] = None  # Optional detour POI: {"name": str, "address": str, "coordinates": [lat, lon]}

# class RouteResponse(BaseModel):
#     routes: List[SingleRoute]
#     explanation: str

# @app.post("/route", response_model=RouteResponse)
# async def compute_route(request: RouteRequest):
#     origin_coord = geo_coder.geocode(request.origin)
#     destination_coord = geo_coder.geocode(request.destination)

#     if not origin_coord or not destination_coord:
#         return {
#             "routes": [],
#             "explanation": "Could not find location coordinates for origin or destination."
#         }

#     if request.detour_poi:
#         detour_coord = tuple(request.detour_poi.get("coordinates"))
#         route_data = routing_agent.compute_route_with_detour(
#             origin_coord, detour_coord, destination_coord, priority=request.priority
#         )
#         raw_routes = [route_data]
#     else:
#         raw_routes = routing_agent.compute_routes(
#             origin_coord,
#             destination_coord,
#             priority=request.priority,
#             alternatives=request.alternatives
#         )

#     routes = []
#     for route in raw_routes:
#         energy, unit = estimate_energy_consumption(
#             route['distance_km'],
#             route['duration_min'],
#             stops=0,
#             elevation_gain_m=0,
#             vehicle_type=request.vehicle_type
#         )
#         route['estimated_consumption'] = energy
#         route['consumption_unit'] = unit
#         routes.append(route)

#     explanation = assistant_agent.generate_explanation(
#         route=[request.origin, request.destination],
#         traffic_data={},
#         energy_estimate=routes[0]['estimated_consumption'] if routes else 0,
#         energy_unit=routes[0]['consumption_unit'] if routes else "",
#         vehicle_type=request.vehicle_type,
#     )

#     if request.detour_poi:
#         explanation += f"\n\nDetour included: {request.detour_poi.get('name')} at {request.detour_poi.get('address')}."

#     explanation += f"\n\nNumber of route alternatives: {len(routes)}"

#     return RouteResponse(routes=routes, explanation=explanation)

# @app.post("/search_poi")
# async def search_poi_endpoint(data: dict):
#     query = data.get("query")
#     proximity = data.get("proximity")  # [lat, lon]
#     if not query or not proximity:
#         return {"results": []}
#     results = poi_agent.search_poi(query, tuple(proximity))
#     return {"results": results}

# import os
# from fastapi import FastAPI, Body
# from pydantic import BaseModel
# from typing import List, Optional
# import sys
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# from agents.routing_agent import RoutingAgent
# from agents.assistant_agent import AssistantAgent
# from agents.geocoder import GeoCoder
# from agents.poi_agent import POIAgent
# from agents.utils import estimate_energy_consumption

# app = FastAPI(title="AutoRoute AI Backend")

# MAPBOX_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN")
# TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")

# routing_agent = RoutingAgent(MAPBOX_TOKEN)
# geo_coder = GeoCoder(MAPBOX_TOKEN)
# assistant_agent = AssistantAgent()
# poi_agent = POIAgent(MAPBOX_TOKEN)

# class SingleRoute(BaseModel):
#     route_coords: List[List[float]]
#     distance_km: float
#     duration_min: float
#     estimated_consumption: float
#     consumption_unit: str

# class RouteRequest(BaseModel):
#     origin: str
#     destination: str
#     vehicle_type: str = "EV"
#     priority: str = "normal"
#     alternatives: bool = True
#     detour_poi: Optional[dict] = None  # Optional detour POI

# class RouteResponse(BaseModel):
#     routes: List[SingleRoute]
#     explanation: str

# @app.post("/geocode")
# async def geocode_endpoint(data: dict = Body(...)):
#     location = data.get("location")
#     if not location:
#         return {"error": "No location provided"}

#     coords = geo_coder.geocode(location)
#     if coords:
#         return {"coordinates": coords}
#     else:
#         return {"error": "Location not found"}

# @app.post("/search_poi")
# async def search_poi_endpoint(data: dict = Body(...)):
#     query = data.get("query")
#     proximity = data.get("proximity")  # [lat, lon]
#     if not query or not proximity:
#         return {"results": []}
#     results = poi_agent.search_poi(query, tuple(proximity))
#     return {"results": results}

# @app.post("/route", response_model=RouteResponse)
# async def compute_route(request: RouteRequest):
#     origin_coord = geo_coder.geocode(request.origin)
#     destination_coord = geo_coder.geocode(request.destination)

#     if not origin_coord or not destination_coord:
#         return {
#             "routes": [],
#             "explanation": "Could not find location coordinates for origin or destination."
#         }

#     if request.detour_poi:
#         detour_coord = tuple(request.detour_poi.get("coordinates"))
#         route_data = routing_agent.compute_route_with_detour(
#             origin_coord, detour_coord, destination_coord, priority=request.priority
#         )
#         raw_routes = [route_data]
#     else:
#         raw_routes = routing_agent.compute_routes(
#             origin_coord,
#             destination_coord,
#             priority=request.priority,
#             alternatives=request.alternatives
#         )

#     routes = []
#     for route in raw_routes:
#         energy, unit = estimate_energy_consumption(
#             route['distance_km'],
#             route['duration_min'],
#             stops=0,
#             elevation_gain_m=0,
#             vehicle_type=request.vehicle_type
#         )
#         route['estimated_consumption'] = energy
#         route['consumption_unit'] = unit
#         routes.append(route)

#     explanation = assistant_agent.generate_explanation(
#         route=[request.origin, request.destination],
#         traffic_data={},
#         energy_estimate=routes[0]['estimated_consumption'] if routes else 0,
#         energy_unit=routes[0]['consumption_unit'] if routes else "",
#         vehicle_type=request.vehicle_type,
#     )

#     if request.detour_poi:
#         explanation += f"\n\nDetour included: {request.detour_poi.get('name')} at {request.detour_poi.get('address')}."

#     explanation += f"\n\nNumber of route alternatives: {len(routes)}"

#     return RouteResponse(routes=routes, explanation=explanation)



import os
from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import List, Optional
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from agents.routing_agent import RoutingAgent
from agents.assistant_agent import AssistantAgent
from agents.geocoder import GeoCoder
from agents.poi_agent import POIAgent
from agents.utils import estimate_energy_consumption
from agents.ConversationAgent import ConversationAgent
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AutoRoute AI Backend")

# Enable CORS for frontend origin(s)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL(s) in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAPBOX_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN")
TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")

routing_agent = RoutingAgent(MAPBOX_TOKEN)
geo_coder = GeoCoder(MAPBOX_TOKEN)
assistant_agent = AssistantAgent()
poi_agent = POIAgent(MAPBOX_TOKEN)
conversation_agent = ConversationAgent()

class SingleRoute(BaseModel):
    route_coords: List[List[float]]
    distance_km: float
    duration_min: float
    estimated_consumption: float
    consumption_unit: str
    detour_poi: Optional[dict] = None

class RouteRequest(BaseModel):
    origin: str
    destination: str
    vehicle_type: str = "EV"
    priority: str = "normal"
    alternatives: bool = True
    detour_poi: Optional[dict] = None

class RouteResponse(BaseModel):
    routes: List[SingleRoute]
    explanation: str

@app.post("/geocode")
async def geocode_endpoint(data: dict = Body(...)):
    location = data.get("location")
    if not location:
        return {"error": "No location provided"}

    coords = geo_coder.geocode(location)
    if coords:
        return {"coordinates": coords}
    else:
        return {"error": "Location not found"}

@app.post("/search_poi")
async def search_poi_endpoint(data: dict = Body(...)):
    query = data.get("query")
    proximity = data.get("proximity")  # [lat, lon]
    if not query or not proximity:
        return {"results": []}
    results = poi_agent.search_poi(query, tuple(proximity))
    return {"results": results}

@app.post("/route", response_model=RouteResponse)
async def compute_route(request: RouteRequest):
    origin_coord = geo_coder.geocode(request.origin)
    destination_coord = geo_coder.geocode(request.destination)

    if not origin_coord or not destination_coord:
        return {
            "routes": [],
            "explanation": "Could not find location coordinates for origin or destination."
        }

    if request.detour_poi:
        detour_coord = tuple(request.detour_poi.get("coordinates"))
        route_data = routing_agent.compute_route_with_detour(
            origin_coord, detour_coord, destination_coord, priority=request.priority
        )
        # Attach detour_poi info to route dict
        route_data["detour_poi"] = request.detour_poi
        raw_routes = [route_data]
    else:
        raw_routes = routing_agent.compute_routes(
            origin_coord,
            destination_coord,
            priority=request.priority,
            alternatives=request.alternatives
        )

    routes = []
    for route in raw_routes:
        energy, unit = estimate_energy_consumption(
            route['distance_km'],
            route['duration_min'],
            stops=0,
            elevation_gain_m=0,
            vehicle_type=request.vehicle_type
        )
        route['estimated_consumption'] = energy
        route['consumption_unit'] = unit
        routes.append(route)

    explanation = assistant_agent.generate_explanation(
        route=[request.origin, request.destination],
        traffic_data={},
        energy_estimate=routes[0]['estimated_consumption'] if routes else 0,
        energy_unit=routes[0]['consumption_unit'] if routes else "",
        vehicle_type=request.vehicle_type,
    )

    if request.detour_poi:
        explanation += f"\n\nDetour included: {request.detour_poi.get('name')} at {request.detour_poi.get('address')}."

    explanation += f"\n\nNumber of route alternatives: {len(routes)}"

    return RouteResponse(routes=routes, explanation=explanation)

@app.post("/chat")
async def chat_endpoint(data: dict = Body(...)):
    user_message = data.get("message")
    context = data.get("context", "")

    if not user_message:
        return {"error": "No message provided"}

    conversation_agent.add_system_message(context)
    conversation_agent.add_user_message(user_message)
    reply = conversation_agent.generate_response()
    return {"reply": reply}
