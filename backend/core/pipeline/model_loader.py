from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

def list_gemini_models():
    """List all available Gemini models from the API."""
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
    
    client = genai.Client(api_key=api_key)
    
    models = client.models.list()
    
    for model in models:
        print(f"Name: {model.name}")
        print(f"Display Name: {model.display_name}")
        print(f"Description: {model.description}")
        print(f"Input Token Limit: {model.input_token_limit}")
        print(f"Output Token Limit: {model.output_token_limit}")
        print("-" * 50)

if __name__ == "__main__":
    list_gemini_models()