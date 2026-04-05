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
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.tools.declarations import TOOL_DECLARATIONS
from core.tools.registry import TOOL_REGISTRY

load_dotenv()

# ======================================================
# CONSTANTES
# ======================================================
CHARACTERS_DIR = Path(__file__).parent.parent / "characters"
HISTORY_FILE   = Path(__file__).parent / "history.json"
MODEL_DEFAULT  = "gemini-2.5-flash-lite"
MODEL_SEARCH   = "gemini-2.0-flash"
MAX_HISTORY    = 20

client: genai.Client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY"),
    http_options={"timeout": 600000}
    )


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
    try:
        # Se text vazio ou só whitespace, usar fallback
        if not text or not text.strip():
            return [_make_fallback(character_name, "...")]

        parsed = json.loads(clean_json(text))

        if isinstance(parsed, dict):
            return [parsed]

        if isinstance(parsed, list) and parsed and isinstance(parsed[0], str):
            return [_make_fallback(character_name, parsed[0])]

        return parsed if parsed else [_make_fallback(character_name, "...")]

    except json.JSONDecodeError:
        return [_make_fallback(character_name, text.strip())] if text.strip() else [_make_fallback(character_name, "...")]


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
        "INSTRUÇÕES:\n"
        "- SEMPRE responda em um JSON array com um objeto.\n"
        f"- Formato: [{{\"character\": \"{character_name}\", \"text\": \"sua resposta aqui\", \"state\": \"neutral\"}}]\n"
        "- Sem texto antes ou depois do JSON.\n"
        "- Português correto. Acentos obrigatórios. Nunca 'nao', sempre 'não'.\n"
        "- Máximo 20 palavras por mensagem (exceto se ensinar algo).\n"
        "- Se ensina algo: máximo 100 palavras.\n"
        "- Se pergunta complexa: máximo 50 palavras.\n"
        f"- Estados válidos: {valid_states}\n"
        "- Use 'text' com a sua resposta natural e direta.\n"
        "- IMPORTANTE: Responda SEMPRE com JSON válido, nada de texto extra."
    )


# ======================================================
# HELPERS — TOOLS
# ======================================================
def get_model_for_character(character: dict) -> str:
    """Usa modelo mais capaz se o personagem tiver web_search."""
    if "web_search" in character.get("tools", []):
        return MODEL_SEARCH
    return MODEL_DEFAULT


def build_tools_for_character(character: dict) -> list | None:
    """Monta a lista de tools do Gemini baseado no JSON do personagem."""
    tool_names = character.get("tools", [])
    if not tool_names:
        return None

    tools = []

    # tools normais — passam pelo execute_tool_call
    other_names = [n for n in tool_names if n != "web_search"]
    declarations = [
        TOOL_DECLARATIONS[name]
        for name in other_names
        if name in TOOL_DECLARATIONS
    ]

    if declarations:
        tools.append(types.Tool(function_declarations=declarations))

    # web_search é especial — SEMPRE em objeto separado, SEMPRE por último
    if "web_search" in tool_names:
        tools.append(types.Tool(google_search=types.GoogleSearch()))

    return tools if tools else None


def execute_tool_call(tool_name: str, args: dict) -> str:
    """Executa a função real e retorna o resultado como string JSON."""
    fn = TOOL_REGISTRY.get(tool_name)
    if not fn:
        return json.dumps({"erro": f"Ferramenta '{tool_name}' não encontrada"})
    try:
        result = fn(**args)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"erro": f"Erro ao executar {tool_name}: {str(e)}"})


def _has_tool_call(response) -> bool:
    """Verifica se o Gemini quer chamar alguma tool."""
    try:
        candidates = response.candidates
        if not candidates:
            return False

        content = candidates[0].content
        if not content or not content.parts:
            return False

        return any(
            hasattr(part, "function_call") and part.function_call
            for part in content.parts
        )
    except (IndexError, AttributeError):
        return False


def _extract_tool_results(response) -> list[types.Part]:
    """Executa as tool calls e retorna os resultados."""
    results = []

    try:
        parts = response.candidates[0].content.parts
        if not parts:
            return results
    except (IndexError, AttributeError):
        return results

    for part in parts:
        if not hasattr(part, "function_call") or not part.function_call:
            continue

        fc     = part.function_call
        result = execute_tool_call(fc.name, dict(fc.args))

        results.append(
            types.Part(
                function_response=types.FunctionResponse(
                    name=fc.name,
                    response={"result": result}
                )
            )
        )

    return results


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
        if not content:
            return []
        data = json.loads(content)
        if not isinstance(data, dict):
            return []
        return data.get(normalize_character_name(character_name), [])
    except json.JSONDecodeError:
        return []


def _append_to_history(history: list, role: Role, content: str) -> None:
    history.append({"role": role, "content": content})


def persist_history(character_name: str, history: list) -> None:
    all_history: dict = {}

    if HISTORY_FILE.exists():
        try:
            content = HISTORY_FILE.read_text(encoding="utf-8")
            if content:
                all_history = json.loads(content)
        except json.JSONDecodeError:
            all_history = {}

    all_history[normalize_character_name(character_name)] = history[-MAX_HISTORY:]
    HISTORY_FILE.write_text(
        json.dumps(all_history, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def clear_history(character_name: str) -> bool:
    if not HISTORY_FILE.exists():
        return False

    key = normalize_character_name(character_name)
    try:
        content = HISTORY_FILE.read_text(encoding="utf-8")
        if not content:
            return False
        all_history = json.loads(content)
    except json.JSONDecodeError:
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
    """Compatibilidade com feed e audio_transcribe que usam chamada direta."""
    try:
        response = client.models.generate_content(
            model=MODEL_DEFAULT,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.7,
            ),
            contents=contents,
        )
        return response.text or ""
    except Exception:
        return json.dumps(
            [
                {
                    "character": character_name,
                    "text": "Desculpe, ocorreu um erro ao processar sua mensagem.",
                    "state": "hushed",
                }
            ]
        )


# ======================================================
# MAIN
# ======================================================
def generate_message(message: str, character_name: str) -> list[dict]:
    """Gera uma mensagem do personagem, com suporte a tool calling."""
    try:
        character = load_character(character_name)
    except FileNotFoundError as e:
        return [_make_fallback(character_name, f"Personagem não encontrado")]

    history = load_history(character_name)
    tools = build_tools_for_character(character)
    model = get_model_for_character(character)

    _append_to_history(history, Role.USER, message)
    contents = _build_contents(history)
    system_prompt = build_system_prompt(character_name, character)

    # ── loop de tool calling ──────────────────────────────
    max_iterations = 5
    raw = None
    response = None

    for iteration in range(1, max_iterations + 1):
        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.7,
            tools=tools or [],
        )

        try:
            response = client.models.generate_content(
                model=model,
                config=config,
                contents=contents
            )
        except Exception as e:
            # Retorna erro específico no primeiro intento, fallback depois
            error_text = str(e)[:50]
            if iteration == 1:
                return [_make_fallback(character_name, f"Erro API: {error_text}")]
            else:
                # Retorna último raw se conseguiu algo, senão fallback
                break

        # resposta vazia ou bloqueada
        if not response or not response.candidates:
            if iteration < max_iterations:
                continue  # Retry
            raw = None
            break

        # sem tool call — resposta final
        if not _has_tool_call(response):
            raw = response.text
            break

        # executa as tools e continua o loop
        tool_results = _extract_tool_results(response)

        if not tool_results:
            raw = response.text
            break

        # Adiciona response ao histórico
        if response.candidates[0].content:
            contents.append(response.candidates[0].content)

        # Adiciona tool results
        contents.append(
            types.Content(role="tool", parts=tool_results)
        )

    # Se saiu do loop sem ter raw, tenta usar a última response
    if raw is None and response:
        raw = response.text
    # ── fim do loop ───────────────────────────────────────

    # Parse resposta (sempre retorna algo válido)
    parsed = parse_response(raw or "", character_name)

    # Garantir que pelo menos há uma resposta
    if not parsed or not parsed[0].get("text") or parsed[0].get("text") == "...":
        parsed = [_make_fallback(character_name, "Recebi sua mensagem!")]

    # Salva histórico
    try:
        _append_to_history(history, Role.MODEL, parsed[0]["text"])
        persist_history(character_name, history)
    except Exception as e:
        print(f"[WARN] Erro ao salvar histórico: {e}")

    return parsed


# ======================================================
# DEBUG
# ======================================================
if __name__ == "__main__":
    print(generate_message("Qual a Selic hoje?", "Corretor Rodrigo"))