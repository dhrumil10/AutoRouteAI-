import os
import openai
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()  # Load environment variables from .env

openai.api_key = os.getenv("OPENAI_API_KEY")

class AssistantAgent:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model

    def generate_explanation(self, route: List[str], traffic_data: Dict) -> str:
        """
        Generate a natural language explanation for the route based on traffic conditions.
        """

        prompt = self._build_prompt(route, traffic_data)

        response = openai.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=200,
        )

        explanation = response.choices[0].message.content.strip()
        return explanation

    def _build_prompt(self, route: List[str], traffic_data: Dict) -> str:
        route_str = " -> ".join(route)
        congestion_info = ", ".join(
            [f"{road}: {traffic_data.get(road, {}).get('congestion', 'unknown')}" for road in route]
        )

        prompt = (
            f"You are a helpful assistant for a smart vehicle routing system.\n"
            f"The current planned route is: {route_str}.\n"
            f"Traffic congestion levels on this route are: {congestion_info}.\n"
            f"Please provide a clear, concise explanation of why this route was chosen, "
            f"mentioning traffic and any detours or optimizations."
        )
        return prompt

# Example usage
if __name__ == "__main__":
    agent = AssistantAgent()
    example_route = ["Origin", "3rd Blvd", "2nd Ave", "Destination"]
    example_traffic = {
        "Origin": {"congestion": "low"},
        "3rd Blvd": {"congestion": "medium"},
        "2nd Ave": {"congestion": "low"},
        "Destination": {"congestion": "low"},
    }
    explanation = agent.generate_explanation(example_route, example_traffic)
    print("Route Explanation:\n", explanation)
