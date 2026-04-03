from pathlib import Path
import pytest
from tests.conftest import Colors

AUDIO_PATH = Path(__file__).parent / "audio_teste.webm"

@pytest.mark.api
def test_transcribe_voice(client, first_character):
    """Test POST /voice/{character}/transcribe transcribes audio and generates response"""
    print(f"\n{Colors.BLUE}Testing: POST /voice/{first_character}/transcribe{Colors.ENDC}")
    
    if not AUDIO_PATH.exists():
        pytest.skip(f"audio_teste.webm não encontrado em {AUDIO_PATH}")

    audio_size = AUDIO_PATH.stat().st_size
    print(f"  Audio file: {AUDIO_PATH.name} ({Colors.YELLOW}{audio_size} bytes{Colors.ENDC})")
    
    with AUDIO_PATH.open("rb") as f:
        response = client.post(
            f"/voice/{first_character}/transcribe",
            files={"audio": ("audio_teste.webm", f, "audio/webm")}
        )

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "transcription" in data, "Response missing 'transcription' field"
    assert "responses" in data, "Response missing 'responses' field"
    assert len(data["transcription"]) > 0, "Empty transcription"
    assert len(data["responses"]) > 0, "No character responses"
    
    print(f"  Status: {Colors.GREEN}{response.status_code}{Colors.ENDC}")
    print(f"  Transcription: '{Colors.CYAN}{data['transcription']}{Colors.ENDC}'")
    print(f"  Character responses: {Colors.YELLOW}{len(data['responses'])}{Colors.ENDC}")
    for i, resp in enumerate(data["responses"][:2], 1):
        char = resp.get('character', 'Unknown')
        mode = resp.get('state', 'neutral')
        text = resp.get('text', '')[:50]
        print(f"    {i}. [{Colors.CYAN}{char}{Colors.ENDC}] ({mode}) {text}...")

@pytest.mark.api
def test_transcribe_unsupported_type(client, first_character):
    """Test POST /voice/{character}/transcribe rejects unsupported audio types"""
    print(f"\n{Colors.BLUE}Testing: POST /voice/{first_character}/transcribe with unsupported type (should fail){Colors.ENDC}")
    
    response = client.post(
        f"/voice/{first_character}/transcribe",
        files={"audio": ("teste.txt", b"conteudo falso", "text/plain")}
    )
    
    assert response.status_code == 415, f"Expected 415, got {response.status_code}"
    print(f"  Status: {Colors.GREEN}{response.status_code}{Colors.ENDC}")
    print(f"  Error: Unsupported media type (expected)")
    print(f"  Details: {response.json().get('detail', 'Unsupported type')}")

@pytest.mark.api
def test_transcribe_audio_too_large(client, first_character):
    """Test POST /voice/{character}/transcribe rejects files larger than 1MB"""
    print(f"\n{Colors.BLUE}Testing: POST /voice/{first_character}/transcribe with large file (should fail){Colors.ENDC}")
    
    audio_grande = b"0" * 1_100_000  # larger than 1MB
    file_size_mb = len(audio_grande) / 1_000_000
    
    response = client.post(
        f"/voice/{first_character}/transcribe",
        files={"audio": ("grande.webm", audio_grande, "audio/webm")}
    )
    
    assert response.status_code == 413, f"Expected 413, got {response.status_code}"
    print(f"  Status: {Colors.GREEN}{response.status_code}{Colors.ENDC}")
    print(f"  File size: {Colors.YELLOW}{file_size_mb:.2f} MB{Colors.ENDC}")
    print(f"  Error: Payload too large (expected)")
    print(f"  Details: {response.json().get('detail', 'File too large')}")