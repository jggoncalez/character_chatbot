from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from core.pipeline.chat import generate_message, load_history, CHARACTERS_DIR
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    character_name: str

class ChatResponse(BaseModel):
    character: str
    text: str
    state: str

@router.get("/characters")
async def get_characters():
    try:
        characters = [f.stem.capitalize() for f in CHARACTERS_DIR.glob("*.json")]
        return {"characters": characters}
    except Exception as e:
        logger.exception("Failed to retrieve characters")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/chat", response_model=List[ChatResponse])
async def chat(request: ChatRequest):
    try:
        responses = generate_message(request.message, request.character_name)
        return responses
    except FileNotFoundError as e:
        logger.exception(
            "Character data not found for name: %s", request.character_name
        )
        raise HTTPException(status_code=404, detail="Character not found")
    except Exception as e:
        logger.exception("Unexpected error during chat request processing")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/history/{character_name}")
async def get_character_history(character_name: str):
    try:
        history = load_history(character_name)
        return {"character": character_name, "history": history}
    except Exception as e:
        logger.exception("Failed to load history for character: %s", character_name)
        raise HTTPException(status_code=500, detail="Internal server error")