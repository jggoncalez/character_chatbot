import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_characters():
    print("\n1. Testando GET /characters...")
    response = requests.get(f"{BASE_URL}/characters")
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.json()}")
    return response.json().get("characters", [])

def test_chat(character: str):
    print(f"\n2. Testando POST /chat com personagem '{character}'...")
    payload = {
        "message": "Olá, tudo bem?",
        "character_name": character
    }
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def test_history(character: str):
    print(f"\n3. Testando GET /history/{character}...")
    response = requests.get(f"{BASE_URL}/history/{character}")
    print(f"Status: {response.status_code}")
    print(f"Histórico recebido para '{character}'")

def test_api():
    print("Iniciando testes da API...")

    try:
        characters = test_characters()
    except Exception as e:
        print(f"Erro em /characters: {e}")
        return

    if not characters:
        print("Nenhum personagem encontrado.")
        return

    character = characters[0]

    try:
        test_chat(character)
    except Exception as e:
        print(f"Erro em /chat: {e}")

    try:
        test_history(character)
    except Exception as e:
        print(f"Erro em /history: {e}")

if __name__ == "__main__":
    test_api()