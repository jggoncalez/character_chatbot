# Character Chatbot API - Test Suite

Complete automated test suite for the Character Chatbot API with comprehensive coverage of all endpoints and functionality.

## 📋 Test Coverage

### Test Files

- **test_character.py** - Character endpoint tests
  - `test_get_characters` - Lists all available characters
  - `test_character_details` - Retrieves character JSON configuration
  - `test_character_details_not_found` - Error handling for non-existent characters

- **test_chat.py** - Chat functionality tests
  - `test_chat_response` - Chat message processing and response generation
  - `test_chat_character_not_found` - Error handling for invalid characters
  - `test_get_history` - Chat history retrieval
  - `test_clear_history` - Chat history cleanup

- **test_feed.py** - Feed/Social media functionality tests
  - `test_get_feed` - On-demand feed generation
  - `test_get_feed_cached` - Cached feed retrieval
  - `test_feed_comment` - Comment posting and character responses
  - `test_feed_comment_not_found` - Error handling for invalid posts

- **test_voice.py** - Voice transcription tests
  - `test_transcribe_voice` - Audio transcription and character response
  - `test_transcribe_unsupported_type` - Rejected unsupported audio formats
  - `test_transcribe_audio_too_large` - File size validation

## 🚀 Running Tests

### Prerequisites

1. Ensure the backend is running:
```bash
cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

2. Install pytest (if not already installed):
```bash
pip install pytest
```

### Run All Tests (Interactive)

```bash
python tests/run_tests.py
```

This launches an interactive menu to select which tests to run.

### Run All Tests (Command Line)

```bash
pytest tests/ -v
```

### Run Specific Test File

```bash
pytest tests/test_chat.py -v
pytest tests/test_voice.py -v
```

### Run Tests by Marker

```bash
# API endpoint tests only
pytest tests/ -m api -v

# Integration tests only
pytest tests/ -m integration -v
```

### Run Specific Test

```bash
pytest tests/test_chat.py::test_chat_response -v
```

### Run with Coverage

```bash
pytest tests/ --cov=core --cov=api --cov-report=html
# View report: open htmlcov/index.html
```

### Run with Output Capture

```bash
# Show print statements
pytest tests/ -v -s

# Show detailed output
pytest tests/ -vv -s
```

## 📊 Test Output Format

Tests provide detailed, color-formatted output including:

- ✓ **Passing tests** - Green checkmarks with status code
- ✗ **Failed tests** - Red X marks with error details
- ⊘ **Skipped tests** - Yellow circles with skip reason
- 📝 **Test details** - API endpoints, parameters, and responses
- 🎯 **Data samples** - Sample data from API responses

Example output:

```
Testing: POST /chat with Inuyasha
  Status: 200
  Input: 'Olá, tudo bem?'
  Character: Inuyasha
  Response: 'O que você quer? Fale logo!'
  Mood: angry
✓ PASSED
```

## 🔧 Configuration

Tests can be configured in `pytest.ini`:

- Test discovery patterns
- Markers and categories
- Logging levels (default: INFO)
- Timeout settings (default: 30s)
- Color output (enabled by default)

## 🧪 Test Fixtures

Available pytest fixtures (from `conftest.py`):

- **`client`** - FastAPI TestClient for making requests
- **`first_character`** - First available character from API
- **`all_characters`** - List of all available characters

Usage example:

```python
def test_example(client, first_character):
    response = client.get(f"/characters/{first_character}/details")
    assert response.status_code == 200
```

## 📈 Best Practices

1. **Always start the server** before running tests
2. **Use markers** for organizing test categories
3. **Run interactive tester** (`run_tests.py`) for better output
4. **Check print statements** with `-s` flag for debugging
5. **Review test output** for API response examples

## 🐛 Troubleshooting

### Tests can't connect
- Ensure API server is running on 127.0.0.1:8000
- Check: `curl http://127.0.0.1:8000/characters`

### Audio transcription tests fail
- Verify `audio_teste.webm` exists in tests folder
- File size: ~28KB

### History/Feed tests fail
- Empty or corrupted `history.json`/`feed.json` files should be treated as empty state
- Check file permissions, file locks, or whether another process is modifying these files during tests

### Import errors
- Ensure you're in the `backend/` directory
- Check that `conftest.py` is in tests folder

## 📝 Example Test Run

```bash
$ pytest tests/test_chat.py::test_chat_response -v

tests/test_chat.py::test_chat_response PASSED
Testing: POST /chat with Inuyasha
  Status: 200
  Input: 'Olá, tudo bem?'
  Character: Inuyasha
  Response: 'O que você quer? Fale logo!'
  Mood: angry
✓ PASSED [100%]
```

## 🎯 Test Statistics

Current test count: **13 tests**
- ✓ API endpoint tests: 7
- ✓ Error handling tests: 6
- Categories: Characters, Chat, Feed, Voice

Target coverage: **>80%** of API endpoints and business logic
