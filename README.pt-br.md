# character_chatbot

> 🇺🇸 [English version](README.md)

Chatbot de personagens de anime/jogos com personalidade definida por arquivos JSON, backend em Python (FastAPI + Gemini) e frontend em Angular.

> ⚠️ Projeto em desenvolvimento. Algumas partes ainda não estão concluídas.

---

## Estrutura do projeto

```
character_chatbot/
├── backend/
│   ├── core/
│   │   ├── characters/        # Perfis dos personagens em JSON
│   │   ├── pipeline/
│   │   │   └── chat.py        # Pipeline principal de geração de mensagens
│   │   └── history.json       # Histórico de conversas (gerado em runtime)
│   ├── api/                   # Rotas da API (em desenvolvimento)
│   ├── main.py                # Entry point FastAPI (em desenvolvimento)
│   └── requirements.txt
└── frontend/                  # Branch: feature/angular
```

---

## Backend

### Tecnologias

- **Python** com **FastAPI**
- **Google Gemini** (`gemini-2.5-flash`) via SDK `google-genai`
- **python-dotenv** para variáveis de ambiente

### Como funciona

O pipeline em `backend/core/pipeline/chat.py` recebe uma mensagem e o nome de um personagem, carrega o perfil JSON correspondente, monta um system prompt com as regras de comportamento e formato, e chama a API do Gemini. A resposta é parseada como JSON estruturado no formato:

```json
[
  {
    "character": "NomeDoPersonagem",
    "text": "Resposta do personagem aqui.",
    "state": "neutral"
  }
]
```

Os estados possíveis são: `happy`, `sad`, `angry`, `neutral`, `hushed`.

O histórico da conversa é persistido por personagem em `history.json`, com limite de 20 entradas.

### Personagens disponíveis

| Personagem | Origem |
|---|---|
| Goku | Dragon Ball Z |
| Inuyasha | Inuyasha |
| Megumin | KonoSuba |
| Shadow the Hedgehog | Sonic the Hedgehog |

### Instalação

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configuração

Crie um arquivo `.env` na raiz do projeto com:

```env
GEMINI_API_KEY=sua_chave_aqui
```

### Executando o pipeline diretamente (debug)

```bash
python backend/core/pipeline/chat.py
```

### Executando a API

> A API ainda está em desenvolvimento.

```bash
# Em breve
fastapi dev backend/main.py
```

---

## Frontend

O frontend está sendo desenvolvido em **Angular** e se encontra na branch `feature/angular`.

```bash
git checkout feature/angular
```

> Em desenvolvimento.

---

## Licença

MIT — veja [LICENSE](LICENSE) para mais detalhes.
