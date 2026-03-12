# ======================================================
# IMPORTS
# ======================================================
import os
import re
import json
from enum import Enum
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# ======================================================
# CONSTANTES
# ======================================================
CHARACTERS_DIR = Path(__file__).parent.parent / "characters"
HISTORY_FILE   = Path(__file__).parent.parent / "history.json"
MODEL_ID       = "gemini-2.5-flash"
MAX_HISTORY    = 20

client: genai.Client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


# ======================================================
# ENUMS
# ======================================================
class Role(str, Enum):
    USER  = "user"
    MODEL = "model"


class State(str, Enum):
    HAPPY   = "happy"
    SAD     = "sad"
    ANGRY   = "angry"
    NEUTRAL = "neutral"
    HUSHED  = "hushed"


# ======================================================
# HELPERS — JSON
# ======================================================
def clean_json(text: str) -> str:
    return re.sub(r"```json|```", "", text).strip()


def parse_response(text: str, character_name: str) -> list[dict]:
    """Tenta parsear a resposta da API. Retorna fallback em caso de erro."""
    try:
        parsed = json.loads(clean_json(text))

        if isinstance(parsed, dict):
            return [parsed]

        if isinstance(parsed, list) and parsed and isinstance(parsed[0], str):
            return [_make_fallback(character_name, parsed[0])]

        return parsed

    except json.JSONDecodeError:
        return [_make_fallback(character_name, text.strip())]


def _make_fallback(character_name: str, text: str) -> dict:
    return {
        "character": character_name,
        "text": text,
        "state": State.NEUTRAL,
    }


# ======================================================
# HELPERS — PERSONAGEM
# ======================================================
def load_character(name: str) -> dict:
    path = CHARACTERS_DIR / (name.lower().replace(" ", "_") + ".json")

    if not path.exists():
        raise FileNotFoundError(f"Personagem '{name}' não encontrado em {path}")

    return json.loads(path.read_text(encoding="utf-8"))


def _build_system_prompt(character_name: str, character: dict) -> str:
    valid_states = ", ".join(s.value for s in State)
    return (
        f"Você é {character_name}.\nPerfil: {character}\n"
        "REGRAS ABSOLUTAS:\n"
        "- Responda SOMENTE com JSON válido, nada mais.\n"
        "- Sem texto antes ou depois do JSON.\n"
        "- Mensagens até 20 palavras, português do Brasil, sem emojis.\n"
        f'FORMATO OBRIGATÓRIO (copie exatamente):\n'
        f'[{{"character": "{character_name}", "text": "sua resposta aqui", "state": "neutral"}}]\n'
        f"Estados válidos: {valid_states}"
    )


# ======================================================
# HELPERS — HISTÓRICO
# ======================================================
def load_history(character_name: str) -> list:
    if not HISTORY_FILE.exists():
        return []

    data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    return data.get(character_name, [])


def _append_to_history(history: list, role: Role, content: str) -> None:
    """Adiciona uma entrada ao histórico em memória."""
    history.append({"role": role, "content": content})


def persist_history(character_name: str, history: list) -> None:
    """Salva o histórico (truncado) em disco."""
    all_history: dict = {}

    if HISTORY_FILE.exists():
        all_history = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))

    all_history[character_name] = history[-MAX_HISTORY:]
    HISTORY_FILE.write_text(
        json.dumps(all_history, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


# ======================================================
# HELPERS — API
# ======================================================
def _build_contents(history: list) -> list[types.Content]:
    return [
        types.Content(role=t["role"], parts=[types.Part(text=t["content"])])
        for t in history[-MAX_HISTORY:]
    ]


def _call_api(contents: list[types.Content], system_prompt: str) -> str:
    response = client.models.generate_content(
        model=MODEL_ID,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.7,
        ),
        contents=contents,
    )
    return response.text or ""


# ======================================================
# MAIN
# ======================================================
def generate_message(message: str, character_name: str) -> list[dict]:
    character = load_character(character_name)
    history   = load_history(character_name)

    _append_to_history(history, Role.USER, message)

    contents       = _build_contents(history)
    system_prompt  = _build_system_prompt(character_name, character)
    raw_response   = _call_api(contents, system_prompt)
    parsed         = parse_response(raw_response, character_name)

    # Guard against malformed API responses that pass through parse_response
    # as arbitrary JSON (e.g. an empty list, or a list whose first element is
    # not a dict, or a dict that is missing the required "text" key).
    # Without this check, parsed[0]["text"] below would raise an IndexError,
    # TypeError, or KeyError respectively.
    valid_parsed = (
        isinstance(parsed, list)       # must be a list ...
        and len(parsed) > 0            # ... that is non-empty ...
        and isinstance(parsed[0], dict)  # ... whose first item is a dict ...
        and "text" in parsed[0]        # ... with the required "text" key.
    )
    if not valid_parsed:
        # The structure is unexpected; fall back to the raw API text so we can
        # still save something meaningful to history and return a response.
        parsed = [_make_fallback(character_name, raw_response)]

    _append_to_history(history, Role.MODEL, parsed[0]["text"])
    persist_history(character_name, history)

    return parsed


# ======================================================
# DEBUG
# ======================================================
if __name__ == "__main__":
    generate_message("Qual é, Shadow!? Sei que tivemos nossas diferenças, mas por quê não comer alguns chilli dogs?", "Shadow")