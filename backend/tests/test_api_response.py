#!/usr/bin/env python3
"""Debug o que a API tá retornando"""
import sys
import os
sys.path.insert(0, '/home/racer/Codes/character_chatbot/backend')

from google import genai
from google.genai import types

# Simple test
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"), http_options={"timeout": 600000})

system_prompt = """Você é Tux.
Perfil: {'name': 'Tux', 'age': '30+', 'personality': {'traits': ['friendly']}}

Responda SEMPRE neste EXATO formato JSON (sem nada antes ou depois):
[{"character": "Tux", "text": "<sua resposta aqui>", "state": "neutral"}]

Regras:
- Responda direto e naturalmente
- Máximo 20 palavras
- Português correto com acentos
- Responda como você, não como um bot
"""

message = "Olá!"

print("Testing API response...")
print(f"System Prompt length: {len(system_prompt)}")
print(f"Message: {message}\n")

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.7,
        ),
        contents=[
            types.Content(
                role="user",
                parts=[types.Part(text=message)]
            )
        ]
    )

    print(f"✓ API Response received")
    print(f"  Candidates: {len(response.candidates) if response.candidates else 0}")
    if response.candidates:
        print(f"  Text: {repr(response.text)[:100]}")
        print(f"  Full text: {response.text}")
    else:
        print(f"  NO CANDIDATES")

except Exception as e:
    print(f"✗ Error: {type(e).__name__}")
    print(f"  {str(e)[:200]}")
    import traceback
    traceback.print_exc()
