# 🎭 character_chatbot

> 🇺🇸 [English version](README.md)

Plataforma de chatbot com personagens icônicos de animes e jogos, com personalidades profundas e persistentes — movida por **Google Gemini**, **FastAPI** e **Angular**.

Desenvolvida como projeto de conclusão do curso **Técnico em Desenvolvimento de Sistemas** pelo **SENAI**.

---

## ✨ Funcionalidades

- 💬 **IA Conversacional** — converse com 11 personagens únicos, cada um com sua própria personalidade, estilo de fala e história
- 🧠 **Tool-Calling** — personagens acessam dados do mundo real (clima, finanças, Wikipedia, ArXiv, feeds de notícias e mais) via ferramentas especializadas
- 📰 **Feed Social** — personagens geram posts autonomamente e respondem aos comentários dos usuários em personagem
- 🎙️ **Entrada por Voz** — transcrição de mensagens de áudio via Gemini
- 🗂️ **Histórico Persistente** — memória de conversa por personagem (últimas 20 mensagens)
- ⚡ **Paralelização Assíncrona** — geração do feed usa `asyncio.gather` para criar posts de múltiplos personagens em paralelo
- 🔒 **Cache com TTL** — cache em memória para chamadas a ferramentas externas, reduzindo latência e consumo de API
- 🌐 **Frontend SSR** — Angular 21 com Server-Side Rendering
- 📄 **Documentação Interativa** — Swagger UI disponível em `/docs`

---

## 🎮 Personagens

| Personagem | Origem | Ferramentas Especiais |
|---|---|---|
| **Goku** | Dragon Ball Z | Clima, data/hora |
| **Inuyasha** | Inuyasha | Clima, data/hora |
| **Megumin** | KonoSuba | Clima, Wikipedia |
| **Shadow the Hedgehog** | Sonic the Hedgehog | Clima, notícias de tecnologia |
| **Abri** | Original | Wikipedia, educação |
| **Corretor Rodrigo** | Original | Finanças (FIIs, Selic, notícias da B3), clima |
| **Dra. Galastriceia Pantufa** | Original | Dados médicos/ANVISA, PubMed, clima |
| **Hiromi Higuruma** | Jujutsu Kaisen | Jurídico (LexML/Planalto), Wikipedia |
| **Pixxie** | Original | Tech (crates.io, kernel RSS, GitHub) |
| **Professor Elcio Veras** | Original | ArXiv, Wikipedia, educação |
| **Tux** | Mascote do Linux | Notícias de tech, kernel RSS, GitHub |

Cada personagem é definido por um perfil JSON contendo traços de personalidade, história, relacionamentos, estilo de fala, fraquezas e ferramentas atribuídas.

---

## 🏗️ Arquitetura

```
character_chatbot/
├── backend/
│   ├── main.py                     # Entry point FastAPI (CORS, rotas)
│   ├── requirements.txt
│   ├── Procfile                    # Configuração de deploy Railway
│   ├── api/
│   │   └── routes.py               # Todos os endpoints REST
│   └── core/
│       ├── characters/             # Um .json por personagem
│       ├── chat/
│       │   └── pipeline.py         # Lógica Gemini + gerenciamento de histórico
│       ├── feed/
│       │   └── pipeline.py         # Geração assíncrona de feed + comentários
│       ├── audio_transcribe/
│       │   └── pipeline.py         # Transcrição de áudio via Gemini
│       └── tools/                  # Módulos de ferramentas por domínio
│           ├── declarations.py     # Declarações de funções para tool-calling do Gemini
│           ├── registry.py         # Mapeia personagens → conjuntos de ferramentas
│           ├── finance/            # BRAPI, Selic (BCB), notícias da B3
│           ├── weather/            # wttr.in
│           ├── wikipedia/          # Wikipedia Summary API
│           ├── arxiv/              # Busca no ArXiv
│           ├── medical/            # ANVISA, PubMed
│           ├── legal/              # LexML / Planalto
│           ├── tech/               # crates.io, kernel.org RSS, GitHub Search
│           ├── education/          # APIs educacionais
│           └── retail/             # RSS de varejo/supermercados
├── frontend/                       # Angular 21 + SSR (Bootstrap 5)
│   ├── Procfile                    # Configuração de deploy Railway
│   └── src/
│       └── app/
│           └── main/
│               ├── features/       # Páginas: feed, chat, perfil
│               └── shared/         # Serviços, interfaces, utilitários
├── docs/
│   ├── api_endpoints_en.md         # Referência completa da API (inglês)
│   └── api_endpoints_pt_br.md      # Referência completa da API (português)
├── makefile                        # Atalhos de desenvolvimento
└── LICENSE
```

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.11+
- Node.js 20+ / npm 11+
- Chave de API do Google Gemini ([obtenha aqui](https://aistudio.google.com/app/apikey))

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/character_chatbot.git
cd character_chatbot
```

### 2. Configure as variáveis de ambiente

Crie um arquivo `.env` dentro da pasta `backend/`:

```env
GEMINI_API_KEY=sua_chave_aqui
```

### 3. Instale as dependências

```bash
make install
```

Ou manualmente:

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

### 4. Execute o projeto

```bash
make run
```

Ou separadamente:

```bash
# Backend
make run-backend   # → http://127.0.0.1:8000

# Frontend
make run-frontend  # → http://localhost:4200
```

**Documentação interativa da API** disponível em: `http://127.0.0.1:8000/docs`

---

## 🔌 Visão Geral da API

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/characters` | Lista todos os personagens disponíveis |
| `POST` | `/chat` | Envia uma mensagem a um personagem |
| `GET` | `/character/{name}/details` | Retorna o perfil JSON completo do personagem |
| `GET` | `/history/{name}` | Retorna o histórico de conversas |
| `DELETE` | `/history/{name}/clear` | Limpa o histórico de um personagem |
| `GET` | `/feed` | Retorna o feed social (gera novos posts) |
| `GET` | `/feed/cached` | Retorna o feed em cache (sem regeneração) |
| `POST` | `/feed/post` | Cria um post do usuário (personagens comentam) |
| `POST` | `/feed/comment` | Comenta em um post (personagem responde) |
| `POST` | `/chat/audio` | Envia áudio — Gemini transcreve e responde |

Referência completa da API em [`docs/api_endpoints_pt_br.md`](docs/api_endpoints_pt_br.md).

---

## 🤖 Como a IA Funciona

### Pipeline de Chat

```
Mensagem do usuário
     ↓
Carrega JSON do personagem (cache lru_cache + deepcopy)
     ↓
Monta system prompt (personalidade + regras de comportamento + formato)
     ↓
Resolve ferramentas do personagem (registry.py)
     ↓
Chama API Gemini (gemini-2.5-flash / gemini-2.0-flash para web search)
     ↓
Parseia resposta JSON estruturada
     ↓
Persiste no arquivo de histórico do personagem
     ↓
Retorna: [{ "character": "...", "text": "...", "state": "..." }]
```

### Pipeline do Feed

```
GET /feed
     ↓
asyncio.gather → todos os personagens geram posts em paralelo
     ↓
Posts salvos em feed.json (com file locking para segurança de concorrência)
     ↓
Usuário comenta → personagem responde automaticamente em sua própria voz
```

### Formato de Resposta

Toda resposta do chat é uma lista JSON estruturada:

```json
[
  {
    "character": "Inuyasha",
    "text": "Tch. De novo você. O que quer?",
    "state": "neutral"
  }
]
```

Estados possíveis: `happy` · `sad` · `angry` · `neutral` · `hushed`

---

## 🛠️ Atalhos do Makefile

```bash
make install          # Instala dependências do backend e frontend
make run              # Inicia backend e frontend ao mesmo tempo
make run-backend      # Inicia FastAPI na porta 8000
make run-frontend     # Inicia servidor de desenvolvimento Angular
make test             # Executa pytest
make clear-history    # Apaga todos os arquivos de histórico de chat
make clear-feed       # Apaga o cache do feed
make clear-data       # Apaga histórico e feed
make clean            # Remove venv e node_modules
```

## 🧪 Testes

```bash
make test
# ou
cd backend && python -m pytest tests/ -v
```

Os testes utilizam `pytest` com `TestClient` do FastAPI e `httpx`.

---

## 🗂️ Stack Tecnológica

| Camada | Tecnologia |
|---|---|
| **IA** | Google Gemini (`gemini-2.5-flash`, `gemini-2.0-flash`) |
| **Backend** | Python 3.11+, FastAPI, google-genai, python-dotenv |
| **Frontend** | Angular 21, SSR, Bootstrap 5, TypeScript |
| **APIs Externas** | BRAPI, Banco Central (BCB), wttr.in, Wikipedia, ArXiv, PubMed, ANVISA, LexML, GitHub Search, crates.io, kernel.org, InfoMoney RSS |

---

## 📜 Licença

MIT — veja [LICENSE](LICENSE) para mais detalhes.