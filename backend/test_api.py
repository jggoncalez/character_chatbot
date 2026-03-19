import requests
import json
import time
import subprocess
import os

def test_api():
    print("Iniciando testes da API...")
    
    # base da API
    base_url = "http://127.0.0.1:8000"
    
  
    print("\n1. Testando GET /characters...")
    try:
        response = requests.get(f"{base_url}/characters")
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.json()}")
        characters = response.json().get("characters", [])
    except Exception as e:
        print(f"Erro ao testar /characters: {e}")
        return

    #  Testar endpoint /chat
    if characters:
        character = characters[0]
        print(f"\n2. Testando POST /chat com personagem {character}...")
        payload = {
            "message": "Olá, tudo bem?",
            "character_name": character
        }
        try:
            response = requests.post(f"{base_url}/chat", json=payload)
            print(f"Status: {response.status_code}")
            print(f"Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        except Exception as e:
            print(f"Erro ao testar /chat: {e}")
    else:
        print("\nNenhum personagem encontrado para testar /chat.")

    # Testar endpoint /history
    if characters:
        character = characters[0]
        print(f"\n3. Testando GET /history/{character}...")
        try:
            response = requests.get(f"{base_url}/history/{character}")
            print(f"Status: {response.status_code}")
            # Não imprime todo o histórico para não poluir o log
            print(f"Histórico recebido para {character}")
        except Exception as e:
            print(f"Erro ao testar /history: {e}")

if __name__ == "__main__":
    test_api()
