import json
import random
from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4
from core.chat.pipeline import load_character, _call_api, _build_system_prompt, CHARACTERS_DIR

FEED_FILE = Path(__file__).parent / "feed.json"
MAX_POSTS = 20          # máximo de posts no feed
MAX_COMMENTS = 3        # comentários por post
POSTS_PER_REFRESH = 2   # posts novos gerados por abertura do feed


# ======================================================
# HELPERS — JSON
# ======================================================
def load_feed() -> list[dict]:
    if not FEED_FILE.exists():
        return []
    return json.loads(FEED_FILE.read_text(encoding="utf-8"))


def save_feed(feed: list[dict]) -> None:
    FEED_FILE.write_text(
        json.dumps(feed, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def _all_character_names() -> list[str]:
    return [f.stem for f in CHARACTERS_DIR.glob("*.json")]


# ======================================================
# GERAÇÃO DE POST
# ======================================================
def _generate_post(character_name: str) -> dict | None:
    """Pede ao Gemini que o personagem crie um post curto sobre seu dia."""
    try:
        character = load_character(character_name)
        system    = _build_system_prompt(character_name, character)

        prompt = (
            "Escreva UM post curto para uma rede social, "
            "como se fosse uma publicação sua hoje. "
            "Máximo 2 frases. Sem hashtags. Fique no personagem."
        )

        from google.genai import types
        contents = [types.Content(role="user", parts=[types.Part(text=prompt)])]
        raw      = _call_api(contents, system, character_name)

        # reutiliza o parse existente
        from core.chat.pipeline import parse_response
        parsed = parse_response(raw, character_name)
        text   = parsed[0].get("text", "").strip()

        if not text:
            return None

        return {
            "id":         str(uuid4()),
            "character":  character_name,
            "text":       text,
            "state":      parsed[0].get("state", "neutral"),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "comments":   [],
        }
    except Exception:
        return None


# ======================================================
# GERAÇÃO DE COMENTÁRIOS
# ======================================================
def _generate_comments(post: dict, all_names: list[str]) -> list[dict]:
    """Sorteia alguns personagens pra comentar no post."""
    candidates = [n for n in all_names if n != post["character"]]
    commenters = random.sample(candidates, min(MAX_COMMENTS, len(candidates)))
    comments   = []

    for commenter in commenters:
        try:
            character = load_character(commenter)
            system    = _build_system_prompt(commenter, character)

            prompt = (
                f"{post['character']} postou: \"{post['text']}\"\n"
                "Escreva UM comentário curto reagindo a isso. "
                "Máximo 1 frase. Fique no personagem."
            )

            from google.genai import types
            from core.chat.pipeline import parse_response, _call_api
            contents = [types.Content(role="user", parts=[types.Part(text=prompt)])]
            raw      = _call_api(contents, system, commenter)
            parsed   = parse_response(raw, commenter)
            text     = parsed[0].get("text", "").strip()

            if text:
                comments.append({
                    "id":         str(uuid4()),
                    "character":  commenter,
                    "text":       text,
                    "state":      parsed[0].get("state", "neutral"),
                    "created_at": datetime.now(timezone.utc).isoformat(),
                })
        except Exception:
            continue

    return comments


# ======================================================
# MAIN — chamado pelo endpoint
# ======================================================
def refresh_feed() -> list[dict]:
    """Gera posts novos, adiciona comentários, persiste e retorna o feed."""
    feed      = load_feed()
    all_names = _all_character_names()

    if not all_names:
        return feed

    # sorteia quais personagens postam nesse refresh
    posters = random.sample(all_names, min(POSTS_PER_REFRESH, len(all_names)))

    for character_name in posters:
        post = _generate_post(character_name)
        if not post:
            continue

        post["comments"] = _generate_comments(post, all_names)
        feed.insert(0, post)   # mais recente primeiro

    # mantém o feed no limite máximo
    feed = feed[:MAX_POSTS]
    save_feed(feed)
    return feed


# ======================================================
# COMENTÁRIO DO USUÁRIO
# ======================================================
def add_user_comment(post_id: str, user_text: str) -> dict | None:
    """Adiciona comentário do usuário e gera 1 resposta do autor do post."""
    feed = load_feed()
    post = next((p for p in feed if p["id"] == post_id), None)

    if not post:
        return None

    # comentário do usuário
    user_comment = {
        "id":         str(uuid4()),
        "character":  "user",
        "text":       user_text,
        "state":      "neutral",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    post["comments"].append(user_comment)

    # autor do post responde ao usuário
    try:
        character = load_character(post["character"])
        system    = _build_system_prompt(post["character"], character)
        prompt    = (
            f"Você postou: \"{post['text']}\"\n"
            f"Um usuário comentou: \"{user_text}\"\n"
            "Responda ao comentário em 1 frase. Fique no personagem."
        )
        from google.genai import types
        from core.chat.pipeline import parse_response, _call_api
        contents = [types.Content(role="user", parts=[types.Part(text=prompt)])]
        raw      = _call_api(contents, system, post["character"])
        parsed   = parse_response(raw, post["character"])
        text     = parsed[0].get("text", "").strip()

        if text:
            post["comments"].append({
                "id":         str(uuid4()),
                "character":  post["character"],
                "text":       text,
                "state":      parsed[0].get("state", "neutral"),
                "created_at": datetime.now(timezone.utc).isoformat(),
            })
    except Exception:
        pass

    save_feed(feed)
    return post