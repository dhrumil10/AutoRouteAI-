# import os
# import openai
# from dotenv import load_dotenv
# from typing import List, Dict

# load_dotenv()  # Load environment variables from .env

# openai.api_key = os.getenv("OPENAI_API_KEY")

# class AssistantAgent:
#     def __init__(self, model: str = "gpt-4o-mini"):
#         self.model = model

#     def generate_explanation(self, route: List[str], traffic_data: Dict) -> str:
#         """
#         Generate a natural language explanation for the route based on traffic conditions.
#         """

#         prompt = self._build_prompt(route, traffic_data)

#         response = openai.chat.completions.create(
#             model=self.model,
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.6,
#             max_tokens=200,
#         )

#         explanation = response.choices[0].message.content.strip()
#         return explanation

#     def _build_prompt(self, route: List[str], traffic_data: Dict) -> str:
#         route_str = " -> ".join(route)
#         congestion_info = ", ".join(
#             [f"{road}: {traffic_data.get(road, {}).get('congestion', 'unknown')}" for road in route]
#         )

#         prompt = (
#             f"You are a helpful assistant for a smart vehicle routing system.\n"
#             f"The current planned route is: {route_str}.\n"
#             f"Traffic congestion levels on this route are: {congestion_info}.\n"
#             f"Please provide a clear, concise explanation of why this route was chosen, "
#             f"mentioning traffic and any detours or optimizations."
#         )
#         return prompt

# # Example usage
# if __name__ == "__main__":
#     agent = AssistantAgent()
#     example_route = ["Origin", "3rd Blvd", "2nd Ave", "Destination"]
#     example_traffic = {
#         "Origin": {"congestion": "low"},
#         "3rd Blvd": {"congestion": "medium"},
#         "2nd Ave": {"congestion": "low"},
#         "Destination": {"congestion": "low"},
#     }
#     explanation = agent.generate_explanation(example_route, example_traffic)
#     print("Route Explanation:\n", explanation)


import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class AssistantAgent:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model

    def generate_explanation(self, route, traffic_data, energy_estimate, energy_unit, vehicle_type):
        prompt = self._build_prompt(route, traffic_data, energy_estimate, energy_unit, vehicle_type)
        response = openai.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=250,
        )
        return response.choices[0].message.content.strip()

    def _build_prompt(self, route, traffic_data, energy_estimate, energy_unit, vehicle_type):
        route_str = " -> ".join(route)
        congestion_info = ", ".join(
            [f"{road}: {traffic_data.get(road, {}).get('congestion', 'unknown')}" for road in route]
        )

        tips_intro = ""
        if vehicle_type.lower() == "ev":
            tips_intro = (
                "As this is an electric vehicle, suggest tips like managing battery usage, "
                "using regenerative braking, and minimizing steep climbs."
            )
        else:
            tips_intro = (
                "As this is a gasoline vehicle, suggest tips like maintaining smooth acceleration, "
                "avoiding idling, and keeping regular maintenance."
            )

        prompt = (
            f"You are a smart assistant for vehicle routing.\n"
            f"The planned route is: {route_str}.\n"
            f"Traffic congestion levels are: {congestion_info}.\n"
            f"The estimated {energy_unit} consumption for this trip is {energy_estimate} {energy_unit}.\n"
            f"Vehicle type: {vehicle_type}.\n"
            f"{tips_intro}\n"
            f"Provide a clear explanation of the route choice and personalized driving tips."
        )
        return prompt
