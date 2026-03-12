import os
import re
import json
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# ═══════════════════════════════════════════
# SETUP
# ═══════════════════════════════════════════

load_dotenv()

CHARACTERS_DIR = Path(__file__).parent.parent / "characters"

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# ═══════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════

def clean_json(text: str) -> str:
    text = re.sub(r"```json|```", "", text)
    return text.strip()


def load_character(name: str) -> dict:
    filename = name.lower().replace(" ", "_") + ".json"
    path     = CHARACTERS_DIR / filename
    return json.loads(path.read_text(encoding="utf-8"))

# ═══════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════

def generate_message(message: str, character_name: str) -> dict:

    character = load_character(character_name)
    
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        config=types.GenerateContentConfig(
            system_instruction=f'''
            Você é {character_name}.
            Regras:
                - Mande mensagens até 20 palavras.
                - Responda em português do Brasil.
                - Sem emojis na mensagem.
                - Linguagem clara, seguindo informações do perfil do personagem.
                
            Perfil do personagem:
            {character}
            
            IMPORTANTE: retorne apenas JSON, sem markdowns, e sem backticks.
            
            FORMATO:
            Format:
            [
                {{"character": "{character_name}", "text": "dialog here", "state": "happy | sad | angry | neutral | hushed}},
            ]
            
            ''',
            temperature=1.0,
        ),
        contents=[f"User message: {message}"]
    )
    try:
        response_text = response.text
        response = json.loads(clean_json(response_text))
        print(f"Mensagem completa: {response}")
    except json.JSONDecodeError:
        print(f"JSON incorreto: {response_text}")
        raise
    return response

if __name__ == "__main__":
    message = "Olá pessoa!"
    character = "Megumin"
    
    generate_message(message, character)
    
    