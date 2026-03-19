import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# Importando a lógica existente sem alterá-la
from core.pipeline.chat import generate_message, load_history, CHARACTERS_DIR

app = FastAPI(title="Character Chatbot API")

# Configuração de CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    character_name: str

class ChatResponse(BaseModel):
    character: str
    text: str
    state: str

@app.get("/characters")
async def get_characters():
    """Lista todos os personagens disponíveis."""
    try:
        characters = [f.stem.capitalize() for f in CHARACTERS_DIR.glob("*.json")]
        return {"characters": characters}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=List[ChatResponse])
async def chat(request: ChatRequest):
    """Envia uma mensagem para um personagem e recebe a resposta."""
    try:
        responses = generate_message(request.message, request.character_name)
        return responses
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/{character_name}")
async def get_character_history(character_name: str):
    """Retorna o histórico de chat para um personagem específico."""
    try:
        history = load_history(character_name)
        return {"character": character_name, "history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
