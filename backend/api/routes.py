from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from typing import List
from fastapi.concurrency import run_in_threadpool
from core.chat.pipeline import generate_message, load_history, CHARACTERS_DIR, load_character, clear_history
from core.feed.pipeline import refresh_feed, add_user_comment, load_feed
from core.audio_transcribe.pipeline import transcribe_audio
import logging

SUPPORTED_TYPES = [
    "audio/webm",
    "audio/webm;codecs=opus",
    "audio/mp4",
    "audio/wav",
    "audio/ogg"
]


logger = logging.getLogger(__name__)

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    character_name: str

class ChatResponse(BaseModel):
    character: str
    text: str
    state: str


class UserCommentRequest(BaseModel):
    post_id: str
    text: str = Field(min_length=1, max_length=500)

@router.get("/characters")
async def get_characters():
    try:
        characters = await run_in_threadpool(
            lambda: [" ".join(word.capitalize() for word in f.stem.replace("_", " ").split()) for f in CHARACTERS_DIR.glob("*.json")]
        )
        return {"characters": characters}
    except Exception as e:
        logger.exception("Failed to retrieve characters")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/chat", response_model=List[ChatResponse])
async def chat(request: ChatRequest):
    try:
        responses = await run_in_threadpool(
            generate_message, request.message, request.character_name
        )
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
        history = await run_in_threadpool(load_history, character_name)
        return {"character": character_name, "history": history}
    except Exception as e:
        logger.exception("Failed to load history for character: %s", character_name)
        raise HTTPException(status_code=500, detail="Internal server error")
    

@router.get("/feed")
async def get_feed():
    """Retorna o feed, gerando posts novos on-demand."""
    try:
        feed = await run_in_threadpool(refresh_feed)
        return {"posts": feed}
    except Exception:
        logger.exception("Erro ao gerar feed")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/feed/cached")
async def get_feed_cached():
    """Retorna o feed sem gerar posts novos — pra paginação."""
    try:
        feed = await run_in_threadpool(load_feed)
        return {"posts": feed}
    except Exception:
        logger.exception("Erro ao ler feed")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/feed/comment")
async def comment_on_post(request: UserCommentRequest):
    """Usuário comenta num post e o personagem responde."""
    try:
        updated_post = await run_in_threadpool(
            add_user_comment, request.post_id, request.text
        )
        if not updated_post:
            raise HTTPException(status_code=404, detail="Post não encontrado")
        return updated_post
    except HTTPException:
        raise
    except Exception:
        logger.exception("Erro ao comentar")
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.get("/character/{character_name}/details")
async def get_character_details(character_name: str):
    """Retorna o JSON completo de configuração do personagem."""
    try:
        # Usa a função que você já tem no pipeline
        details = await run_in_threadpool(load_character, character_name)
        return details
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Personagem {character_name} não encontrado")
    except Exception as e:
        logger.exception("Erro ao carregar detalhes do personagem")
        raise HTTPException(status_code=500, detail="Erro interno ao carregar JSON")

@router.delete("/history/{character_name}/clear")
async def clear_character_history(character_name: str):
    """Limpa o histórico de chat de um personagem específico."""
    try:
        found = await run_in_threadpool(clear_history, character_name)
        if found:
            return {"message": f"Histórico de {character_name} limpo com sucesso."}
        return {"message": f"Nenhum histórico encontrado para {character_name}."}
    except Exception:
        logger.exception("Erro ao limpar histórico")
        raise HTTPException(status_code=500, detail="Erro ao processar limpeza de arquivo")
    

@router.post("/voice/{character_name}/transcribe")
async def transcribe_voice(
    character_name: str,
    audio: UploadFile = File(...),
):
    try:
        mime = audio.content_type or "audio/webm"
        if not any(mime.startswith(t) for t in SUPPORTED_TYPES):
            raise HTTPException(status_code=415, detail=f"Tipo não suportado: {mime}")
        
        audio_bytes = await audio.read()
        if len(audio_bytes) > 1_000_000:
            raise HTTPException(status_code=413, detail="Áudio muito longo")
        
        text = await run_in_threadpool(transcribe_audio, audio_bytes, mime)
        
        if not text:
            raise HTTPException(status_code=422, detail="Não foi possível transcrever")
        
        responses = await run_in_threadpool(generate_message, text, character_name)
        
        return {"transcription": text, "responses": responses}

    except HTTPException:
        raise
    except FileNotFoundError:
        logger.exception("Character data not found for name: %s", character_name)
        raise HTTPException(status_code=404, detail="Character not found")
    except Exception:
        logger.exception("Erro na transcrição")
        raise HTTPException(status_code=500, detail="Erro interno na transcrição")