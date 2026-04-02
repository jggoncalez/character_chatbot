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
HISTORY_FILE   = Path(__file__).parent / "history.json"
MODEL_ID       = "gemini-2.5-flash-lite"
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


def build_system_prompt(character_name: str, character: dict) -> str:
    valid_states = ", ".join(s.value for s in State)
    return (
        f"Você é {character_name}.\nPerfil: {character}\n"
        "REGRAS ABSOLUTAS:\n"
        "- Responda SOMENTE com JSON válido, nada mais.\n"
        "- Sem texto antes ou depois do JSON.\n"
        "- Português do Brasil UTF-8, sem emojis, sem formatação.\n"
        "- OBRIGATÓRIO: Use português do Brasil CORRETO. "
        "Acentos, cedilha e pontuação são OBRIGATÓRIOS. "
        "Nunca escreva 'nao', sempre 'não'. Nunca 'voce', sempre 'você'.\n"
        "- Padrão: máximo 20 palavras por mensagem.\n"
        "- EXCEÇÃO: Se ensinar algo ou passo a passo, máximo 100 palavras totais.\n"
        "- EXCEÇÃO: Se responder pergunta complexa, máximo 50 palavras.\n"
        "- Sempre priorize concisão e clareza.\n"
        f'FORMATO OBRIGATÓRIO (copie exatamente):\n'
        f'[{{"character": "{character_name}", "text": "sua resposta aqui", "state": "neutral"}}]\n'
        f"Estados válidos: {valid_states}\n"
        "Respeite rigorosamente o limite de palavras especificado para cada contexto."
    )


# ======================================================
# HELPERS — HISTÓRICO
# ======================================================
def normalize_character_name(character_name: str) -> str:
    return character_name.lower().replace(" ", "_")


def load_history(character_name: str) -> list:
    if not HISTORY_FILE.exists():
        return []

    try:
        content = HISTORY_FILE.read_text(encoding="utf-8")
        if not content:  # Handle empty file
            return []
        data = json.loads(content)
        return data.get(normalize_character_name(character_name), [])
    except json.JSONDecodeError:
        # File is corrupted, return empty history
        return []


def _append_to_history(history: list, role: Role, content: str) -> None:
    """Adiciona uma entrada ao histórico em memória."""
    history.append({"role": role, "content": content})


def persist_history(character_name: str, history: list) -> None:
    """Salva o histórico (truncado) em disco."""
    all_history: dict = {}

    if HISTORY_FILE.exists():
        try:
            content = HISTORY_FILE.read_text(encoding="utf-8")
            if content:  # Only parse if not empty
                all_history = json.loads(content)
        except json.JSONDecodeError:
            # File is corrupted, start with empty dict
            all_history = {}

    all_history[normalize_character_name(character_name)] = history[-MAX_HISTORY:]
    HISTORY_FILE.write_text(
        json.dumps(all_history, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def clear_history(character_name: str) -> bool:
    """Remove o histórico de um personagem específico. Retorna True se havia histórico."""
    if not HISTORY_FILE.exists():
        return False

    key = normalize_character_name(character_name)
    try:
        content = HISTORY_FILE.read_text(encoding="utf-8")
        if not content:  # Handle empty file
            return False
        all_history = json.loads(content)
    except json.JSONDecodeError:
        # File is corrupted
        return False

    if key not in all_history:
        return False

    del all_history[key]
    HISTORY_FILE.write_text(
        json.dumps(all_history, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return True


# ======================================================
# HELPERS — API
# ======================================================
def _build_contents(history: list) -> list[types.Content]:
    return [
        types.Content(role=t["role"], parts=[types.Part(text=t["content"])])
        for t in history[-MAX_HISTORY:]
    ]


def call_api(contents: list[types.Content], system_prompt: str, character_name: str) -> str:
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.7,
            ),
            contents=contents,
        )
        return response.text or ""
    except Exception as e:
        return json.dumps([{"character": "{character_name}", "text": "Desculpe, ocorreu um erro ao processar sua mensagem.","state": "hushed"}])


# ======================================================
# MAIN
# ======================================================
def generate_message(message: str, character_name: str) -> list[dict]:
    character = load_character(character_name)
    history   = load_history(character_name)

    _append_to_history(history, Role.USER, message)

    contents       = _build_contents(history)
    system_prompt  = build_system_prompt(character_name, character)
    raw_response   = call_api(contents, system_prompt, character_name)
    parsed         = parse_response(raw_response, character_name)

    _append_to_history(history, Role.MODEL, parsed[0]["text"])
    persist_history(character_name, history)

    return parsed


# ======================================================
# DEBUG
# ======================================================
if __name__ == "__main__":
    generate_message("Pode me dar o passo a passo?", "pixxie")