import json
import random
import threading
import asyncio
import sys
from contextlib import contextmanager
from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4

_current_dir = Path(__file__).parent
if str(_current_dir.parent.parent) not in sys.path:
    sys.path.insert(0, str(_current_dir.parent.parent))

from core.chat.pipeline import load_character, build_system_prompt, CHARACTERS_DIR, client, parse_response
from google.genai import types

try:
    import fcntl  # type: ignore[attr-defined]
except ImportError:
    fcntl = None  # type: ignore[assignment]

try:
    import msvcrt  # type: ignore[attr-defined]
except ImportError:
    msvcrt = None  # type: ignore[assignment]

FEED_FILE = Path(__file__).parent / "feed.json"
MAX_POSTS = 20          # máximo de posts no feed
MAX_COMMENTS = 3        # comentários por post
POSTS_PER_REFRESH = 1   # posts novos gerados por abertura do feed

_feed_thread_lock = threading.Lock()


@contextmanager
def _feed_file_lock():
    """Advisory file lock for FEED_FILE operations (POSIX and Windows)."""
    lock_path = FEED_FILE.with_suffix(".lock")
    lock_file = lock_path.open("a")
    try:
        if fcntl is not None:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        elif msvcrt is not None:
            msvcrt.locking(lock_file.fileno(), msvcrt.LK_LOCK, 1)
        yield
    finally:
        try:
            if fcntl is not None:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
            elif msvcrt is not None:
                msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)
        finally:
            lock_file.close()


# ======================================================
# HELPERS — JSON
# ======================================================
def load_feed() -> list[dict]:
    if not FEED_FILE.exists():
        return []
    with _feed_file_lock():
        try:
            content = FEED_FILE.read_text(encoding="utf-8")
            if not content:  # Handle empty file
                return []
            parsed = json.loads(content)
            if not isinstance(parsed, list):
                return []
            if not all(isinstance(entry, dict) for entry in parsed):
                return []
            return parsed
        except json.JSONDecodeError:
            # File is corrupted, return empty feed
            return []


def save_feed(feed: list[dict]) -> None:
    data = json.dumps(feed, ensure_ascii=False, indent=2)
    tmp_path = FEED_FILE.with_suffix(".json.tmp")
    with _feed_file_lock():
        tmp_path.write_text(data, encoding="utf-8")
        tmp_path.replace(FEED_FILE)


def _all_character_names() -> list[str]:
    return [f.stem for f in CHARACTERS_DIR.glob("*.json")]


# ======================================================
# GERAÇÃO DE POST (ASYNC)
# ======================================================
async def _generate_post_async(character_name: str) -> dict | None:
    """Pede ao Gemini que o personagem crie um post curto sobre seu dia (async)."""
    try:
        character = load_character(character_name)
        system    = build_system_prompt(character_name, character)

        prompt = (
            "Escreva UM post curto para uma rede social, "
            "como se fosse uma publicação sua hoje. "
            "Máximo 2 frases. Sem hashtags. Fique no personagem."
        )

        contents = [types.Content(role="user", parts=[types.Part(text=prompt)])]
        response = await asyncio.to_thread(
            lambda: client.models.generate_content(
                model="gemini-2.5-flash-lite",
                config=types.GenerateContentConfig(
                    system_instruction=system,
                    temperature=0.5,
                ),
                contents=contents,
            )
        )
        raw = response.text if response else ""

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
# GERAÇÃO DE COMENTÁRIOS (ASYNC)
# ======================================================
async def _generate_comment_async(commenter: str, post: dict) -> dict | None:
    """Gera um comentário individual para um post (async)."""
    try:
        character = load_character(commenter)
        system    = build_system_prompt(commenter, character)

        prompt = (
            f"{post['character']} postou: \"{post['text']}\"\n"
            "Escreva UM comentário curto reagindo a esta publicação. "
            "Máximo 1 frase. Fique no personagem."
        )

        contents = [types.Content(role="user", parts=[types.Part(text=prompt)])]
        response = await asyncio.to_thread(
            lambda: client.models.generate_content(
                model="gemini-2.5-flash-lite",
                config=types.GenerateContentConfig(
                    system_instruction=system,
                    temperature=0.5,
                ),
                contents=contents,
            )
        )
        raw = response.text if response else ""

        parsed = parse_response(raw, commenter)
        text   = parsed[0].get("text", "").strip()

        if not text:
            return None

        return {
            "id":         str(uuid4()),
            "character":  commenter,
            "text":       text,
            "state":      parsed[0].get("state", "neutral"),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
    except Exception:
        return None


async def _generate_comments_async(post: dict, all_names: list[str]) -> list[dict]:
    """Gera comentários em paralelo usando asyncio.gather (async)."""
    candidates = [n for n in all_names if n != post["character"]]
    commenters = random.sample(candidates, min(MAX_COMMENTS, len(candidates)))

    # Executa todos os comentários em paralelo
    tasks = [_generate_comment_async(commenter, post) for commenter in commenters]
    results = await asyncio.gather(*tasks, return_exceptions=False)

    # Filtra Nones (comentários que falharam)
    return [comment for comment in results if comment is not None]


# ======================================================
# MAIN — chamado pelo endpoint (ASYNC)
# ======================================================
async def _refresh_feed_async() -> list[dict]:
    """Gera posts novos com comentários em paralelo (async)."""
    with _feed_thread_lock:
        feed      = load_feed()
        all_names = _all_character_names()

        if not all_names:
            return feed

        # sorteia quais personagens postam nesse refresh
        posters = random.sample(all_names, min(POSTS_PER_REFRESH, len(all_names)))

        # Gera posts em paralelo
        post_tasks = [_generate_post_async(character_name) for character_name in posters]
        posts = await asyncio.gather(*post_tasks, return_exceptions=False)

        # Para cada post válido, gera comentários em paralelo
        valid_posts = [p for p in posts if p]

        for post in valid_posts:
            post["comments"] = await _generate_comments_async(post, all_names)
            feed.insert(0, post)   # mais recente primeiro

        # mantém o feed no limite máximo
        feed = feed[:MAX_POSTS]
        save_feed(feed)
        return feed


def refresh_feed() -> list[dict]:
    """Wrapper síncrono para _refresh_feed_async."""
    return asyncio.run(_refresh_feed_async())


# ======================================================
# INTERAÇÕES DO USUÁRIO (ASYNC)
# ======================================================

async def _add_user_post_async(user_text: str) -> dict | None:
    """Usuário cria um post e recebe comentários dos personagens (async)."""
    with _feed_thread_lock:
        feed      = load_feed()
        all_names = _all_character_names()

        if not all_names:
            return None

        # cria o post do usuário
        post = {
            "id":         str(uuid4()),
            "character":  "user",
            "text":       user_text.strip(),
            "state":      "neutral",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "comments":   [],
        }

        # gera comentários de 2-3 personagens em paralelo
        post["comments"] = await _generate_comments_async(post, all_names)

        # adiciona ao feed (mais recente primeiro)
        feed.insert(0, post)
        feed = feed[:MAX_POSTS]
        save_feed(feed)

        return post


def add_user_post(user_text: str) -> dict | None:
    """Wrapper síncrono para _add_user_post_async."""
    return asyncio.run(_add_user_post_async(user_text))


def add_user_comment(post_id: str, user_text: str) -> dict | None:
    """Adiciona comentário do usuário e gera 1 resposta do autor do post (async-compatible)."""
    return asyncio.run(_add_user_comment_async(post_id, user_text))


async def _add_user_comment_async(post_id: str, user_text: str) -> dict | None:
    """Adiciona comentário do usuário e gera 1 resposta do autor do post (async)."""
    with _feed_thread_lock:
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
            system    = build_system_prompt(post["character"], character)
            prompt    = (
                f"Você postou: \"{post['text']}\"\n"
                f"Um usuário comentou: \"{user_text}\"\n"
                "Responda ao comentário em 1 frase. Fique no personagem."
            )

            contents = [types.Content(role="user", parts=[types.Part(text=prompt)])]
            response = await asyncio.to_thread(
                lambda: client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    config=types.GenerateContentConfig(
                        system_instruction=system,
                        temperature=0.5,
                    ),
                    contents=contents,
                )
            )
            raw = response.text if response else ""

            parsed = parse_response(raw, post["character"])
            text   = parsed[0].get("text", "").strip()

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


# ======================================================
# POST DO USUÁRIO
# ======================================================
async def _create_user_post_async(user_text: str) -> dict | None:
    """Usuário cria um post e recebe comentários dos personagens (async)."""
    with _feed_thread_lock:
        feed      = load_feed()
        all_names = _all_character_names()

        if not all_names:
            return None

        # cria o post do usuário
        post = {
            "id":         str(uuid4()),
            "character":  "user",
            "text":       user_text.strip(),
            "state":      "neutral",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "comments":   [],
        }

        # gera comentários de 2-3 personagens em paralelo
        post["comments"] = await _generate_comments_async(post, all_names)

        # adiciona ao feed (mais recente primeiro)
        feed.insert(0, post)
        feed = feed[:MAX_POSTS]
        save_feed(feed)

        return post


def create_user_post(user_text: str) -> dict | None:
    """Wrapper síncrono para _create_user_post_async."""
    return asyncio.run(_create_user_post_async(user_text))


# ======================================================
# TESTE
# ======================================================
if __name__ == "__main__":
    import sys

    print("=== Feed Pipeline Test ===\n")

    # Listar personagens disponíveis
    characters = _all_character_names()
    text = sys.argv[2] if len(sys.argv) > 2 else "O que vocês acham de chocolate com menta?"
    print(f"Criando post do usuário: {text}\n")
    post = create_user_post(text)
    if post:
        print(f"Post criado com {len(post['comments'])} comentários:")
        for comment in post['comments']:
            print(f"  - {comment['character']}: {comment['text']}")