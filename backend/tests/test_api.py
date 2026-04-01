import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def run_characters():
    print("\n1. Testando GET /characters...")
    response = requests.get(f"{BASE_URL}/characters")
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.json()}")
    return response.json().get("characters", [])

def run_chat(character: str):
    print(f"\n2. Testando POST /chat com personagem '{character}'...")
    payload = {
        "message": "Olá, tudo bem?",
        "character_name": character
    }
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def run_history(character: str):
    print(f"\n3. Testando GET /history/{character}...")
    response = requests.get(f"{BASE_URL}/history/{character}")
    print(f"Status: {response.status_code}")
    print(f"Histórico recebido para '{character}'")

def run_feed():
    print("\n4. Testando GET /feed...")
    response = requests.get(f"{BASE_URL}/feed")
    print(f"Status: {response.status_code}")
    # Retornamos o JSON inteiro para poder extrair um post e testar o comentário depois
    return response.json()

def run_feed_cached():
    print("\n5. Testando GET /feed/cached...")
    response = requests.get(f"{BASE_URL}/feed/cached")
    print(f"Status: {response.status_code}")

def run_feed_comment(post_id: str):
    print(f"\n6. Testando POST /feed/comment no post '{post_id}'...")
    payload = {
        "post_id": post_id,
        "text": "Este é um comentário de teste gerado pelo script!"
    }
    response = requests.post(f"{BASE_URL}/feed/comment", json=payload)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def run_api():
    print("Iniciando testes da API...")

    # --- TESTES DE PERSONAGENS E CHAT ---
    try:
        characters = run_characters()
    except Exception as e:
        print(f"Erro em /characters: {e}")
        characters = []

    if characters:
        character = characters[0]
        try:
            test_character_details(character)
            test_clear_history(character)
            run_chat(character)
        except Exception as e:
            print(f"Erro em /chat: {e}")

        try:
            run_history(character)
        except Exception as e:
            print(f"Erro em /history: {e}")
    else:
        print("Nenhum personagem encontrado. Pulando testes de /chat e /history.")

    # --- TESTES DO FEED E COMENTÁRIOS ---
    try:
        feed_data = run_feed()
        posts = feed_data.get("posts", [])
    except Exception as e:
        print(f"Erro em /feed: {e}")
        posts = []

    try:
        run_feed_cached()
    except Exception as e:
        print(f"Erro em /feed/cached: {e}")
        
    

    # Tenta usar um post do feed para testar o comentário
    if posts:
        primeiro_post = posts[0]
        # Tenta pegar a chave "id" ou "post_id" (dependendo de como seu backend retorna o ID do post)
        post_id = primeiro_post.get("id") or primeiro_post.get("post_id")
        
        if post_id:
            try:
                run_feed_comment(str(post_id))
            except Exception as e:
                print(f"Erro em /feed/comment: {e}")
        else:
            print("\nNão foi possível extrair um 'id' ou 'post_id' do primeiro post retornado para testar o comentário.")
    else:
        print("\nNenhum post foi retornado do feed. Pulando o teste de /feed/comment.")

def test_character_details(character: str):
    print(f"\n7. Testando GET /character/{character}/details...")
    response = requests.get(f"{BASE_URL}/character/{character}/details")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Detalhes de '{character}' carregados com sucesso (JSON OK).")

def test_clear_history(character: str):
    print(f"\n8. Testando DELETE /history/{character}/clear...")
    response = requests.delete(f"{BASE_URL}/history/{character}/clear")
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.json().get('message')}")


if __name__ == "__main__":
    run_api()
    