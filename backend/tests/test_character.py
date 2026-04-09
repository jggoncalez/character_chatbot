import pytest
from tests.conftest import Colors

@pytest.mark.api
def test_get_characters(client):
    """Test GET /characters endpoint returns list of characters"""
    print(f"\n{Colors.BLUE}Testing: GET /characters{Colors.ENDC}")
    response = client.get("/characters")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "characters" in data, "Response missing 'characters' field"
    assert len(data["characters"]) > 0, "No characters returned"
    
    print(f"  Status: {Colors.GREEN}{response.status_code}{Colors.ENDC}")
    print(f"  Total characters: {Colors.CYAN}{len(data['characters'])}{Colors.ENDC}")
    for i, char in enumerate(data["characters"][:5], 1):
        print(f"    {i}. {char}")
    if len(data["characters"]) > 5:
        print(f"    ... and {len(data['characters']) - 5} more")

@pytest.mark.api
def test_character_details(client, first_character):
    """Test GET /character/{name}/details returns character JSON"""
    print(f"\n{Colors.BLUE}Testing: GET /character/{first_character}/details{Colors.ENDC}")
    response = client.get(f"/character/{first_character}/details")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "name" in data, "Response missing 'name' field"
    
    print(f"  Status: {Colors.GREEN}{response.status_code}{Colors.ENDC}")
    print(f"  Character Name: {Colors.CYAN}{data.get('name', 'N/A')}{Colors.ENDC}")
    print(f"  Fields: {', '.join(data.keys())}")

@pytest.mark.api
def test_character_details_not_found(client):
    """Test GET /character/{name}/details with non-existent character"""
    print(f"\n{Colors.BLUE}Testing: GET /character/NonExistentChar/details (should fail){Colors.ENDC}")
    response = client.get("/character/NonExistentCharacter123/details")
    
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    print(f"  Status: {Colors.GREEN}{response.status_code}{Colors.ENDC}")
    print(f"  Expected error: Character not found")