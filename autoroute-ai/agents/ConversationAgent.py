import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class ConversationAgent:
    def __init__(self, model="gpt-4o-mini"):
        self.model = model
        self.conversation_history = []

    def add_user_message(self, message: str):
        self.conversation_history.append({"role": "user", "content": message})

    def add_system_message(self, message: str):
        self.conversation_history.append({"role": "system", "content": message})

    def generate_response(self):
        system_prompt = (
            "You are a helpful AI assistant for a smart route optimizer app. "
            "Answer user questions clearly and helpfully, including driving tips, "
            "route info, eco-driving advice, and app usage."
        )
        messages = [{"role": "system", "content": system_prompt}] + self.conversation_history
        response = openai.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=250,
        )
        assistant_msg = response.choices[0].message.content.strip()
        self.conversation_history.append({"role": "assistant", "content": assistant_msg})
        return assistant_msg
