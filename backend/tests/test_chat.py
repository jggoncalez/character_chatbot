import pytest
from tests.conftest import Colors

@pytest.mark.api
def test_chat_response(client, first_character):
    """Test POST /chat returns proper response with character text and state"""
    print(f"\n{Colors.BLUE}Testing: POST /chat with {first_character}{Colors.ENDC}")
    
    payload = {
        "message": "Olá, tudo bem?",
        "character_name": first_character
    }
    response = client.post("/chat", json=payload)
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert isinstance(data, list), f"Expected list, got {type(data)}"
    assert len(data) > 0, "Empty response from chat"
    assert "text" in data[0], "Response missing 'text' field"
    assert "state" in data[0], "Response missing 'state' field"
    assert "character" in data[0], "Response missing 'character' field"
    
    print(f"  Status: {Colors.GREEN}{response.status_code}{Colors.ENDC}")
    print(f"  Input: '{payload['message']}'")
    print(f"  Character: {Colors.CYAN}{data[0]['character']}{Colors.ENDC}")
    print(f"  Response: '{data[0]['text']}'")
    print(f"  Mood: {Colors.YELLOW}{data[0]['state']}{Colors.ENDC}")

@pytest.mark.api
def test_chat_character_not_found(client):
    """Test POST /chat with non-existent character returns 404"""
    print(f"\n{Colors.BLUE}Testing: POST /chat with non-existent character (should fail){Colors.ENDC}")
    
    response = client.post("/chat", json={
        "message": "Olá",
        "character_name": "PersonagemQueNaoExiste123"
    })
    
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    print(f"  Status: {Colors.GREEN}{response.status_code}{Colors.ENDC}")
    print(f"  Error: {response.json().get('detail', 'Character not found')}")

@pytest.mark.api
def test_get_history(client, first_character):
    """Test GET /history/{character} returns chat history"""
    print(f"\n{Colors.BLUE}Testing: GET /history/{first_character}{Colors.ENDC}")
    
    response = client.get(f"/history/{first_character}")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "history" in data, "Response missing 'history' field"
    assert "character" in data, "Response missing 'character' field"
    
    print(f"  Status: {Colors.GREEN}{response.status_code}{Colors.ENDC}")
    print(f"  Character: {Colors.CYAN}{data['character']}{Colors.ENDC}")
    print(f"  History entries: {Colors.YELLOW}{len(data['history'])}{Colors.ENDC}")
    if data['history']:
        for i, entry in enumerate(data['history'][:3], 1):
            role = entry.get('role', 'unknown')
            content = entry.get('content', '')[:50]
            print(f"    {i}. [{role}] {content}...")

@pytest.mark.api
def test_clear_history(client, first_character):
    """Test DELETE /history/{character}/clear clears chat history"""
    print(f"\n{Colors.BLUE}Testing: DELETE /history/{first_character}/clear{Colors.ENDC}")
    
    response = client.delete(f"/history/{first_character}/clear")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "message" in data, "Response missing 'message' field"
    
    print(f"  Status: {Colors.GREEN}{response.status_code}{Colors.ENDC}")
    print(f"  Message: {Colors.CYAN}{data['message']}{Colors.ENDC}")