from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from fastapi.concurrency import run_in_threadpool
from core.chat.pipeline import generate_message, load_history, CHARACTERS_DIR
from core.feed.pipeline import refresh_feed, add_user_comment, load_feed
from core.chat.pipeline import generate_message, load_history, CHARACTERS_DIR, load_character
import logging, os, json

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
        # O caminho do histórico geralmente segue o padrão do seu load_history
        # Ajuste o caminho se o seu pipeline salvar em outro lugar
        history_file = CHARACTERS_DIR.parent / "chat" / "history.json"
        
        if not history_file.exists():
            return {"message": "Histórico já está vazio (arquivo não existe)."}

        with open(history_file, "r+", encoding="utf-8") as f:
            data = json.load(f)
            # Remove a chave do personagem se ela existir
            if character_name in data:
                del data[character_name]
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
                return {"message": f"Histórico de {character_name} limpo com sucesso."}
            
        return {"message": f"Nenhum histórico encontrado para {character_name}."}
    except Exception as e:
        logger.exception("Erro ao limpar histórico")
        raise HTTPException(status_code=500, detail="Erro ao processar limpeza de arquivo")