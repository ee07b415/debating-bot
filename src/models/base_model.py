# src/models/base_model.py
from transformers import AutoModelForCausalLM, AutoTokenizer
from anthropic import Anthropic
import os

class BaseModel:
    def __init__(self):
        # Initialize Anthropic client with your API key
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        
    async def generate_response(self, prompt):
        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-latest",  # or use other Claude models
                max_tokens=1000,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Sorry, there was an error generating the response."