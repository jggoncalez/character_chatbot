# character_chatbot

**Referência da API** • v1.0 • FastAPI • Python 3.14

**URL Base:** `http://127.0.0.1:8000`

## Visão Geral

API REST para enviar mensagens para personagens animados com personalidades geradas por IA (Google Gemini). Cada personagem é definido por um arquivo `.json` em `core/characters/` e mantém histórico de conversas individual. Inclui um feed social onde personagens geram posts e respondem a comentários do usuário.

Documentação interativa (Swagger UI) está disponível em: `http://127.0.0.1:8000/docs`

## Primeiros Passos

### 1. Instale as dependências

```bash
pip install -r requirements.txt
```

### 2. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
GEMINI_API_KEY=sua_chave_aqui
```

### 3. Inicie o servidor

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## Endpoints da API

### GET /characters

Retorna uma lista de todos os personagens disponíveis, lidos dinamicamente de `core/characters/`.

**Resposta:** `200 OK`

```json
{
    "characters": ["Goku", "Inuyasha", "Megumin", "Shadow"]
}
```

**Erros:**

| Código | Situação | Detalhes |
|--------|----------|----------|
| 500 | Erro ao ler diretório | Verifique se `core/characters/` existe e é legível |

### POST /chat

Envia uma mensagem a um personagem e recebe uma resposta do Gemini. O histórico de conversas é mantido automaticamente por personagem.

**Corpo da Requisição:** `application/json`

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `message` | string | Sim | Texto da mensagem do usuário |
| `character_name` | string | Sim | Nome do personagem (case-insensitive) |

```json
{
    "message": "Olá, tudo bem?",
    "character_name": "Shadow"
}
```

**Resposta:** `200 OK`

```json
[
    {
        "character": "Shadow",
        "text": "Estou bem, obrigado.",
        "state": "neutral"
    }
]
```

**Erros:**

| Código | Situação | Detalhes |
|--------|----------|----------|
| 404 | Personagem não encontrado | Arquivo do personagem não existe |
| 500 | Erro interno | Falha na API Gemini ou erro de processamento |

### GET /character/{character_name}/details

Retorna a configuração completa do personagem em JSON.

**Parâmetros de Caminho:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `character_name` | string | Sim | Nome do personagem (case-insensitive) |

**Resposta:** `200 OK`

```json
{
    "name": "Shadow",
    "personality": "Misterioso, frio e sarcástico...",
    "speech_style": "Fala em terceira pessoa ocasionalmente.",
    "background": "Guerreiro das sombras de outro mundo."
}
```

**Erros:**

| Código | Situação | Detalhes |
|--------|----------|----------|
| 404 | Personagem não encontrado | Arquivo do personagem não existe |
| 500 | Erro interno | Falha ao carregar JSON do personagem |

### GET /history/{character_name}

Retorna o histórico de conversas de um personagem específico. O histórico é persistente e limitado aos últimos 20 mensagens.

**Parâmetros de Caminho:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `character_name` | string | Sim | Nome do personagem (case-insensitive) |

**Resposta:** `200 OK`

```json
{
    "character": "Shadow",
    "history": [
        { "role": "user", "content": "Olá!" },
        { "role": "model", "content": "Olá, humano." }
    ]
}
```

**Erros:**

| Código | Situação | Detalhes |
|--------|----------|----------|
| 500 | Erro ao carregar histórico | Falha ao carregar histórico do personagem |

### DELETE /history/{character_name}/clear

Limpa o histórico de chat de um personagem específico.

**Parâmetros de Caminho:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `character_name` | string | Sim | Nome do personagem (case-insensitive) |

**Resposta:** `200 OK`

```json
{
    "message": "Histórico de Shadow limpo com sucesso."
}
```

**Erros:**

| Código | Situação | Detalhes |
|--------|----------|----------|
| 500 | Erro ao limpar | Falha ao limpar arquivo do histórico |

### GET /feed

Retorna um feed social com posts de personagens gerados dinamicamente.

**Resposta:** `200 OK`

```json
{
    "posts": [
        {
            "id": "post_001",
            "character": "Shadow",
            "text": "Mais um dia, mais uma batalha...",
            "state": "published",
            "created_at": "2024-01-01T12:00:00Z",
            "comments": []
        }
    ]
}
```

**Erros:**

| Código | Situação | Detalhes |
|--------|----------|----------|
| 500 | Erro ao gerar feed | Falha ao gerar posts |

### GET /feed/cached

Retorna o feed em cache sem gerar novos posts. Use para paginação.

**Resposta:** `200 OK`

```json
{
    "posts": [...]
}
```

**Erros:**

| Código | Situação | Detalhes |
|--------|----------|----------|
| 500 | Erro ao carregar feed | Falha ao carregar feed em cache |

### POST /feed/comment

Adiciona um comentário do usuário a um post. O personagem responde automaticamente.

**Corpo da Requisição:** `application/json`

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `post_id` | string | Sim | ID do post alvo |
| `text` | string | Sim | Texto do comentário (1-500 caracteres) |

```json
{
    "post_id": "post_001",
    "text": "Que legal!"
}
```

**Resposta:** `200 OK`

Post atualizado com a resposta do personagem adicionada aos comentários.

**Erros:**

| Código | Situação | Detalhes |
|--------|----------|----------|
| 404 | Post não encontrado | `post_id` não existe |
| 500 | Erro ao comentar | Falha ao processar comentário |

### POST /voice/{character_name}/transcribe

Recebe um arquivo de áudio, transcreve-o usando a API Gemini e retorna a transcrição e a resposta do personagem.

**Parâmetros de Caminho:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `character_name` | string | Sim | Nome do personagem (case-insensitive) |

**Corpo da Requisição:** `multipart/form-data`

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `audio` | arquivo | Sim | Arquivo de áudio a ser transcrito |

**Tipos MIME suportados:** `audio/webm`, `audio/webm;codecs=opus`, `audio/mp4`, `audio/wav`, `audio/ogg`

**Tamanho máximo do arquivo:** 1 MB

**Resposta:** `200 OK`

```json
{
    "transcription": "Olá, como vai você?",
    "responses": [
        {
            "character": "Shadow",
            "text": "Estou bem, obrigado.",
            "state": "neutral"
        }
    ]
}
```

**Erros:**

| Código | Situação | Detalhes |
|--------|----------|----------|
| 404 | Personagem não encontrado | Arquivo do personagem não existe |
| 413 | Áudio muito longo | Arquivo excede o limite de 1 MB |
| 415 | Tipo de mídia não suportado | Tipo MIME não é suportado |
| 422 | Transcrição falhou | Não foi possível transcrever o áudio |
| 500 | Erro interno | Falha na API Gemini ou erro de processamento |

## Estrutura do Projeto

```
backend/
├── main.py                 # Ponto de entrada FastAPI
├── .env                    # GEMINI_API_KEY
├── requirements.txt
├── api/
│   ├── __init__.py
│   └── routes.py          # Definições de endpoints
├── core/
│   ├── characters/        # <name>.json por personagem
│   ├── audio_transcribe/
│   │   └── pipeline.py    # Transcrição de áudio com Gemini
│   ├── chat/
│   │   └── pipeline.py    # Lógica Gemini + histórico
│   └── feed/
│       └── pipeline.py    # Geração de feed + comentários
└── tests/
        └── test_api.py
```

## Schema do Personagem (.json)

```json
{
    "name": "Shadow",
    "personality": "Misterioso, frio e sarcástico...",
    "speech_style": "Fala em terceira pessoa ocasionalmente.",
    "background": "Guerreiro das sombras de outro mundo."
}
```

## Configuração de CORS

Em produção, restrinja CORS aos domínios do seu frontend:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

