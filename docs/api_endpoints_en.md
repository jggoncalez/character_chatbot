# character_chatbot

**API Reference** • v1.0 • FastAPI • Python 3.14

**Base URL:** `http://127.0.0.1:8000`

## Overview

REST API for sending messages to animated characters with AI-generated personalities (Google Gemini). Each character is defined by a `.json` file in `core/characters/` and maintains individual conversation history. Includes a social feed where characters generate posts and respond to user comments.

Interactive documentation (Swagger UI) is available at: `http://127.0.0.1:8000/docs`

## Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_key_here
```

### 3. Start the server

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## API Endpoints

### GET /characters

Returns a list of all available characters, dynamically read from `core/characters/`.

**Response:** `200 OK`

```json
{
    "characters": ["Goku", "Inuyasha", "Megumin", "Shadow"]
}
```

**Errors:**

| Code | Situation | Details |
|------|-----------|---------|
| 500 | Directory read error | Verify `core/characters/` exists and is readable |

### POST /chat

Sends a message to a character and receives a response from Gemini. Conversation history is maintained automatically per character.

**Request Body:** `application/json`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | string | Yes | User message text |
| `character_name` | string | Yes | Character name (case-insensitive) |

```json
{
    "message": "Olá, tudo bem?",
    "character_name": "Shadow"
}
```

**Response:** `200 OK`

```json
[
    {
        "character": "Shadow",
        "text": "Estou bem, obrigado.",
        "state": "neutral"
    }
]
```

**Errors:**

| Code | Situation | Details |
|------|-----------|---------|
| 404 | Character not found | Character file doesn't exist |
| 500 | Internal error | Gemini API failure or processing error |

### GET /character/{character_name}/details

Returns the complete character configuration JSON.

**Path Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `character_name` | string | Yes | Character name (case-insensitive) |

**Response:** `200 OK`

```json
{
    "name": "Shadow",
    "personality": "Misterioso, frio e sarcástico...",
    "speech_style": "Fala em terceira pessoa ocasionalmente.",
    "background": "Guerreiro das sombras de outro mundo."
}
```

**Errors:**

| Code | Situation | Details |
|------|-----------|---------|
| 404 | Character not found | Character file doesn't exist |
| 500 | Internal error | Failed to load character JSON |

### GET /history/{character_name}

Returns the conversation history for a specific character. History is persisted and limited to the last 20 messages.

**Path Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `character_name` | string | Yes | Character name (case-insensitive) |

**Response:** `200 OK`

```json
{
    "character": "Shadow",
    "history": [
        { "role": "user", "content": "Olá!" },
        { "role": "model", "content": "Olá, humano." }
    ]
}
```

**Errors:**

| Code | Situation | Details |
|------|-----------|---------|
| 500 | History load error | Failed to load character history |

### DELETE /history/{character_name}/clear

Clears the chat history for a specific character.

**Path Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `character_name` | string | Yes | Character name (case-insensitive) |

**Response:** `200 OK`

```json
{
    "message": "Histórico de Shadow limpo com sucesso."
}
```

**Errors:**

| Code | Situation | Details |
|------|-----------|---------|
| 500 | Clear error | Failed to clear history file |

### GET /feed

Returns a social feed with dynamically generated character posts.

**Response:** `200 OK`

```json
{
    "posts": [
        {
            "id": "post_001",
            "character": "Shadow",
            "content": "Mais um dia, mais uma batalha...",
            "comments": []
        }
    ]
}
```

**Errors:**

| Code | Situation | Details |
|------|-----------|---------|
| 500 | Feed generation error | Failed to generate posts |

### GET /feed/cached

Returns the cached feed without generating new posts. Use for pagination.

**Response:** `200 OK`

```json
{
    "posts": [...]
}
```

**Errors:**

| Code | Situation | Details |
|------|-----------|---------|
| 500 | Feed load error | Failed to load cached feed |

### POST /feed/comment

Adds a user comment to a post. The character automatically responds.

**Request Body:** `application/json`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `post_id` | string | Yes | Target post ID |
| `text` | string | Yes | Comment text (1-500 characters) |

```json
{
    "post_id": "post_001",
    "text": "Que legal!"
}
```

**Response:** `200 OK`

Updated post with character's response added to comments.

**Errors:**

| Code | Situation | Details |
|------|-----------|---------|
| 404 | Post not found | `post_id` doesn't exist |
| 500 | Comment error | Failed to process comment |

## Project Structure

```
backend/
├── main.py                 # FastAPI entry point
├── .env                    # GEMINI_API_KEY
├── requirements.txt
├── api/
│   ├── __init__.py
│   └── routes.py          # Endpoint definitions
├── core/
│   ├── characters/        # <name>.json per character
│   ├── chat/
│   │   └── pipeline.py    # Gemini logic + history
│   ├── feed/
│   │   └── pipeline.py    # Feed generation + comments
│   └── history.json
└── tests/
        └── test_api.py
```

## Character Schema (.json)

```json
{
    "name": "Shadow",
    "personality": "Misterioso, frio e sarcástico...",
    "speech_style": "Fala em terceira pessoa ocasionalmente.",
    "background": "Guerreiro das sombras de outro mundo."
}
```

## CORS Configuration

In production, restrict CORS to your frontend domains:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

