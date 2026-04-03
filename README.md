# character_chatbot

> 🇧🇷 [Versão em Português](README.pt-br.md)

Chatbot featuring anime/game characters with personalities defined by JSON profiles, Python backend (FastAPI + Gemini), and an Angular frontend.

> ⚠️ Work in progress. Some parts are not yet complete.

---

## Project structure

```
character_chatbot/
│   .gitignore               # Files and folders ignored by Git
│   LICENSE                  # Project MIT license
│   README.md                # Main documentation (English)
│   README.pt-br.md          # Documentation in Portuguese
│
├───backend
│   │   main.py              # FastAPI entry point (CORS, routers)
│   │   requirements.txt     # Python dependencies
│   │
│   ├───api
│   │       .gitkeep         # Keeps the folder tracked by Git
│   │       routes.py        # Endpoints: GET /characters, POST /chat, GET /history
│   │       __init__.py      # Marks the directory as a Python package
│   │
│   ├───core
│   │   │   history.example.json     # Example of the conversation history format
│   │   │
│   │   ├───characters
│   │   │       goku.json        # Goku's personality profile
│   │   │       inuyasha.json    # Inuyasha's personality profile
│   │   │       megumin.json     # Megumin's personality profile
│   │   │       shadow.json      # Shadow's personality profile
│   │   │
│   │   └───pipeline
│   │           chat.py          # Core pipeline: loads character, calls Gemini, persists history
│   │           model_loader.py  # Utility to list available models from the Gemini API
│   │           __init__.py      # Marks the directory as a Python package
│   │
│   └───tests
│           test_api.py      # Manual endpoint tests via requests
│
├───docs
│       api_endpoints.docx   # API endpoints documentation
│
└───frontend                 # Angular frontend (branch: feature/angular)
```

---

## Backend

### Stack

- **Python** with **FastAPI**
- **Google Gemini** (`gemini-2.5-flash`) via `google-genai` SDK
- **python-dotenv** for environment variables

### How it works

The pipeline in `backend/core/pipeline/chat.py` receives a message and a character name, loads the corresponding JSON profile, builds a system prompt with behavior and format rules, and calls the Gemini API. The response is parsed as structured JSON in the following format:

```json
[
  {
    "character": "CharacterName",
    "text": "Character response here.",
    "state": "neutral"
  }
]
```

Valid states: `happy`, `sad`, `angry`, `neutral`, `hushed`.

Conversation history is persisted per character in `history.json`, capped at 20 entries.

### Available characters

| Character | Origin |
|---|---|
| Goku | Dragon Ball Z |
| Inuyasha | Inuyasha |
| Megumin | KonoSuba |
| Shadow the Hedgehog | Sonic the Hedgehog |

### Installation

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

Create a `.env` file at the project root:

```env
GEMINI_API_KEY=your_key_here
```

### Running the pipeline directly (debug)

```bash
python backend/core/pipeline/chat.py
```

### Running the API

> The API is still under development.

```bash
# Coming soon
fastapi dev backend/main.py
```

---

## Frontend

The frontend is being built with **Angular** and lives in the `feature/angular` branch.

```bash
git checkout feature/angular
```

> In development.

---

## License

MIT — see [LICENSE](LICENSE) for details.
