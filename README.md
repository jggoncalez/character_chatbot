# 🎭 character_chatbot

> 🇧🇷 [Versão em Português](README.pt-br.md)

An AI-powered chatbot platform featuring iconic anime and game characters with deep, persistent personalities — powered by **Google Gemini**, **FastAPI**, and **Angular**.

Built as a final project for the **SENAI Systems Development** program.

---

## ✨ Features

- 💬 **Conversational AI** — chat with 11 unique characters, each with their own personality, speech style, and background
- 🧠 **Tool-Calling** — characters can access real-world data (weather, finance, Wikipedia, arXiv, news feeds, and more) via specialized tools
- 📰 **Social Feed** — characters autonomously generate posts and respond to user comments in character
- 🎙️ **Voice Input** — audio message transcription via Gemini
- 🗂️ **Persistent History** — per-character conversation memory (last 20 messages)
- ⚡ **Async Parallelization** — feed generation uses `asyncio.gather` for fast multi-character post generation
- 🔒 **TTL Caching** — in-memory cache for external tool calls to reduce latency and API usage
- 🌐 **SSR Frontend** — Angular 21 with Server-Side Rendering
- 📄 **Interactive API Docs** — Swagger UI available at `/docs`

---

## 🎮 Characters

| Character | Origin | Specialty Tools |
|---|---|---|
| **Goku** | Dragon Ball Z | Weather, date/time |
| **Inuyasha** | Inuyasha | Weather, date/time |
| **Megumin** | KonoSuba | Weather, Wikipedia |
| **Shadow the Hedgehog** | Sonic the Hedgehog | Weather, tech news |
| **Abri** | Original | Wikipedia, education |
| **Corretor Rodrigo** | Original | Finance (FIIs, Selic, B3 news), weather |
| **Dra. Galastriceia Pantufa** | Original | Medical/ANVISA data, PubMed, weather |
| **Hiromi Higuruma** | Jujutsu Kaisen | Legal (LexML/Planalto), Wikipedia |
| **Pixxie** | Original | Tech (crates.io, kernel RSS, GitHub) |
| **Professor Elcio Veras** | Original | ArXiv, Wikipedia, education |
| **Tux** | Linux Mascot | Tech news, kernel RSS, GitHub |

Each character is defined by a JSON profile containing personality traits, background, relationships, speech style, weaknesses, and tool assignments.

---

## 🏗️ Architecture

```
character_chatbot/
├── backend/
│   ├── main.py                     # FastAPI entry point (CORS, routers)
│   ├── requirements.txt
│   ├── Procfile                    # Railway deployment config
│   ├── api/
│   │   └── routes.py               # All REST endpoints
│   └── core/
│       ├── characters/             # One .json per character
│       ├── chat/
│       │   └── pipeline.py         # Gemini chat logic + history management
│       ├── feed/
│       │   └── pipeline.py         # Async feed generation + comment handling
│       ├── audio_transcribe/
│       │   └── pipeline.py         # Audio transcription via Gemini
│       └── tools/                  # Tool modules by domain
│           ├── declarations.py     # Function declarations for Gemini tool-calling
│           ├── registry.py         # Maps character names → tool sets
│           ├── finance/            # BRAPI, Selic (BCB), B3 news
│           ├── weather/            # wttr.in
│           ├── wikipedia/          # Wikipedia summary API
│           ├── arxiv/              # ArXiv search
│           ├── medical/            # ANVISA, PubMed
│           ├── legal/              # LexML / Planalto
│           ├── tech/               # crates.io, kernel.org RSS, GitHub Search
│           ├── education/          # Educational APIs
│           └── retail/             # Retail/supermarket RSS feeds
├── frontend/                       # Angular 21 + SSR (Bootstrap 5)
│   ├── Procfile                    # Railway deployment config
│   └── src/
│       └── app/
│           └── main/
│               ├── features/       # Pages: feed, chat, profile
│               └── shared/         # Services, interfaces, utilities
├── docs/
│   ├── api_endpoints_en.md         # Full API reference (English)
│   └── api_endpoints_pt_br.md      # Full API reference (Portuguese)
├── makefile                        # Dev shortcuts
└── LICENSE
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+ / npm 11+
- Google Gemini API key ([get one here](https://aistudio.google.com/app/apikey))

### 1. Clone the repository

```bash
git clone https://github.com/your-username/character_chatbot.git
cd character_chatbot
```

### 2. Configure environment variables

Create a `.env` file inside the `backend/` folder:

```env
GEMINI_API_KEY=your_key_here
```

### 3. Install dependencies

```bash
make install
```

Or manually:

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### 4. Run the project

```bash
make run
```

Or separately:

```bash
# Backend
make run-backend   # → http://127.0.0.1:8000

# Frontend
make run-frontend  # → http://localhost:4200
```

**Interactive API docs** available at: `http://127.0.0.1:8000/docs`

---

## 🔌 API Overview

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/characters` | List all available characters |
| `POST` | `/chat` | Send a message to a character |
| `GET` | `/character/{name}/details` | Get a character's full JSON profile |
| `GET` | `/history/{name}` | Get conversation history |
| `DELETE` | `/history/{name}/clear` | Clear a character's history |
| `GET` | `/feed` | Get the social feed (generates new posts) |
| `GET` | `/feed/cached` | Get the cached feed (no regeneration) |
| `POST` | `/feed/post` | Create a user post (characters comment on it) |
| `POST` | `/feed/comment` | Comment on a post (character replies) |
| `POST` | `/chat/audio` | Send audio — Gemini transcribes and responds |

Full API reference in [`docs/api_endpoints_en.md`](docs/api_endpoints_en.md).

---

## 🤖 How the AI Works

### Chat Pipeline

```
User message
     ↓
Load character JSON (cached via lru_cache + deepcopy)
     ↓
Build system prompt (personality + behavior + format rules)
     ↓
Resolve tool set for this character (registry.py)
     ↓
Call Gemini API (gemini-2.5-flash / gemini-2.0-flash for web search)
     ↓
Parse structured JSON response
     ↓
Persist to per-character history file
     ↓
Return: [{ "character": "...", "text": "...", "state": "..." }]
```

### Feed Pipeline

```
GET /feed
     ↓
asyncio.gather → all characters generate posts in parallel
     ↓
Posts saved to feed.json (with file locking for concurrency safety)
     ↓
User comments → character auto-replies in their own voice
```

### Response Format

Every chat response is a structured JSON list:

```json
[
  {
    "character": "Inuyasha",
    "text": "Tch. You again. What do you want?",
    "state": "neutral"
  }
]
```

Valid states: `happy` · `sad` · `angry` · `neutral` · `hushed`

---

## 🛠️ Makefile Shortcuts

```bash
make install          # Install backend + frontend dependencies
make run              # Start backend and frontend concurrently
make run-backend      # Start FastAPI on port 8000
make run-frontend     # Start Angular dev server
make test             # Run pytest
make clear-history    # Delete all chat history files
make clear-feed       # Delete the feed cache
make clear-data       # Delete both history and feed
make clean            # Remove venv and node_modules
```

## 🧪 Testing

```bash
make test
# or
cd backend && python -m pytest tests/ -v
```

Tests use `pytest` with `TestClient` from FastAPI and `httpx`.

---

## 🗂️ Tech Stack

| Layer | Technology |
|---|---|
| **AI** | Google Gemini (`gemini-2.5-flash`, `gemini-2.0-flash`) |
| **Backend** | Python 3.11+, FastAPI, google-genai, python-dotenv |
| **Frontend** | Angular 21, SSR, Bootstrap 5, TypeScript |
| **External APIs** | BRAPI, Banco Central (BCB), wttr.in, Wikipedia, ArXiv, PubMed, ANVISA, LexML, GitHub Search, crates.io, kernel.org, InfoMoney RSS |

---

## 📜 License

MIT — see [LICENSE](LICENSE) for details.