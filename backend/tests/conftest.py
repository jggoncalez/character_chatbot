import pytest
from fastapi.testclient import TestClient
from main import app
import sys

# ANSI color codes for better output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

@pytest.fixture(scope="session")
def client():
    """FastAPI test client fixture"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}Initializing Test Client...{Colors.ENDC}")
    return TestClient(app)

@pytest.fixture(scope="session")
def first_character(client):
    """Get first available character from API"""
    try:
        response = client.get("/characters")
        assert response.status_code == 200
        characters = response.json().get("characters", [])
        assert characters, "Nenhum personagem encontrado"
        print(f"{Colors.GREEN}✓ Characters loaded: {', '.join(characters[:3])}...{Colors.ENDC}")
        return characters[0]
    except AssertionError as e:
        print(f"{Colors.RED}✗ Failed to load characters: {e}{Colors.ENDC}")
        raise

@pytest.fixture(scope="session")
def all_characters(client):
    """Get all available characters from API"""
    response = client.get("/characters")
    return response.json().get("characters", [])

def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "api: mark test as API endpoint test"
    )

def pytest_runtest_logreport(report):
    """Format test output with colors"""
    if report.when == "call":
        if report.outcome == "passed":
            print(f"{Colors.GREEN}✓ PASSED{Colors.ENDC}")
        elif report.outcome == "failed":
            print(f"{Colors.RED}✗ FAILED{Colors.ENDC}")
        elif report.outcome == "skipped":
            print(f"{Colors.YELLOW}⊘ SKIPPED{Colors.ENDC}")