# ======================================================
# IMPORTS
# ======================================================
import os
import re
import json
import logging
import threading
from enum import Enum
from pathlib import Path
from functools import lru_cache
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.tools.declarations import TOOL_DECLARATIONS
from core.tools.registry import TOOL_REGISTRY

load_dotenv()

logger = logging.getLogger(__name__)

# ======================================================
# CONSTANTES
# ======================================================
CHARACTERS_DIR = Path(__file__).parent.parent / "characters"
HISTORY_FILE   = Path(__file__).parent / "history.json"
MODEL_DEFAULT  = "gemini-2.5-flash-lite"
MODEL_SEARCH   = "gemini-2.5-flash"
MAX_HISTORY    = 20

client: genai.Client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)

# Per-character lock for history file I/O (never held across I/O of unrelated chars)
_history_locks_guard: threading.Lock = threading.Lock()
_history_locks: dict[str, threading.Lock] = {}
_history_cache: dict[str, list] = {}
_system_prompt_cache: dict[str, str] = {}


def _get_history_lock(key: str) -> threading.Lock:
    with _history_locks_guard:
        if key not in _history_locks:
            _history_locks[key] = threading.Lock()
        return _history_locks[key]


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
        if not text or not text.strip():
            return [_make_fallback(character_name, "")]

        text = text.strip()
        cleaned = clean_json(text)

        parsed = json.loads(cleaned)

        if isinstance(parsed, dict):
            if parsed.get("text"):
                return [parsed]
            return [_make_fallback(character_name, json.dumps(parsed))]

        if isinstance(parsed, list) and parsed:
            if isinstance(parsed[0], dict):
                return parsed
            elif isinstance(parsed[0], str):
                return [_make_fallback(character_name, parsed[0])]

        return [_make_fallback(character_name, "Hmm, não consegui responder agora.")]

    except json.JSONDecodeError:
        if text and text.strip():
            text_clean = text.strip().strip('"').strip("'")
            if text_clean and len(text_clean) > 2:
                return [_make_fallback(character_name, text_clean)]
        return [_make_fallback(character_name, "Desculpe, não consegui processar sua mensagem.")]


def _make_fallback(character_name: str, text: str) -> dict:
    return {
        "character": character_name,
        "text": text,
        "state": State.NEUTRAL,
    }


# ======================================================
# HELPERS — PERSONAGEM
# ======================================================
@lru_cache(maxsize=32)
def load_character(name: str) -> dict:
    path = CHARACTERS_DIR / (name.lower().replace(" ", "_") + ".json")

    if not path.exists():
        raise FileNotFoundError(f"Personagem '{name}' não encontrado em {path}")

    return json.loads(path.read_text(encoding="utf-8"))


def build_system_prompt(character_name: str, character: dict) -> str:
    if character_name in _system_prompt_cache:
        return _system_prompt_cache[character_name]

    valid_states = ", ".join(s.value for s in State)

    result = (
        f"Você é {character_name}.\n"
        f"Perfil: {character}\n\n"
        f"RESPONDA SEMPRE neste formato JSON exato (sem nada antes ou depois):\n"
        f'[{{"character": "{character_name}", "text": "sua resposta aqui", "state": "neutral"}}]\n\n'
        f"Instruções:\n"
        f"- Responda como o personagem naturalmente\n"
        f"- Máximo 20 palavras (ou 100 se ensinar algo)\n"
        f"- Português correto com acentos\n"
        f"- Estados válidos: {valid_states}\n"
        f"- Se perguntarem hora/data, use a ferramenta data_hora_atual\n"
        f"- Se perguntarem clima, use a ferramenta clima_atual\n"
        f"- SEMPRE use o resultado das ferramentas. Nunca substitua dados de ferramentas pelo seu próprio conhecimento\n"
        f"- Nunca invente informações que existem ferramentas para buscar\n"
        f"- PRIORIDADE DAS FERRAMENTAS: sempre prefira as ferramentas específicas disponíveis. "
        f"Use web_search APENAS como último recurso, quando nenhuma outra ferramenta cobrir a pergunta"
    )
    _system_prompt_cache[character_name] = result
    return result


# ======================================================
# HELPERS — TOOLS
# ======================================================
def build_tools_for_character(character: dict) -> tuple[list | None, list | None]:
    """Retorna (fn_tools, search_tools) separados para uso em duas fases."""
    tool_names = character.get("tools", [])
    if not tool_names:
        return None, None

    has_web_search = "web_search" in tool_names
    other_names = [n for n in tool_names if n != "web_search"]

    declarations = [
        TOOL_DECLARATIONS[name]
        for name in other_names
        if name in TOOL_DECLARATIONS
    ]

    fn_tools = [types.Tool(function_declarations=declarations)] if declarations else None
    search_tools = [types.Tool(google_search=types.GoogleSearch())] if has_web_search else None

    return fn_tools, search_tools


def execute_tool_call(tool_name: str, args: dict) -> str:
    fn = TOOL_REGISTRY.get(tool_name)
    if not fn:
        return json.dumps({"erro": f"Ferramenta '{tool_name}' não encontrada"})
    args_display = ", ".join(f"{k}={repr(v)}" for k, v in args.items())
    print(f"[TOOL] 🔧 {tool_name}({args_display})", flush=True)
    try:
        result = fn(**args)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"erro": f"Erro ao executar {tool_name}: {str(e)}"})


def _log_grounding_if_used(response) -> None:
    try:
        meta = response.candidates[0].grounding_metadata
        if not meta:
            return
        queries = getattr(meta, "web_search_queries", None)
        if queries:
            print(f"[TOOL] 🔍 web_search → {', '.join(queries)}", flush=True)
    except (IndexError, AttributeError):
        pass


def _has_tool_call(response) -> bool:
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


def _extract_tool_data(contents: list) -> str | None:
    """Extrai o primeiro resultado real (sem erro) das tool calls nos contents."""
    for c in contents:
        if not hasattr(c, 'role') or c.role != "tool":
            continue
        for part in c.parts:
            if not hasattr(part, 'function_response'):
                continue
            result = part.function_response.response.get("result", "")
            if result and '"erro"' not in result:
                return result
    return None


def _retry_simple_response(
    character_name: str,
    character: dict,
    history: list,
    system_prompt: str,
    tool_data: str = None,
) -> list[dict]:
    """Retry mantendo histórico mas sem tools.

    Se tool_data for fornecido, injeta os dados reais no contexto para o modelo
    responder com dados verdadeiros em vez de alucinar.
    Se não houver dados, instrui o modelo a informar a indisponibilidade.
    """
    print(f"[RETRY] Tentando resposta simples (sem tools)...", flush=True)

    for retry_attempt in range(1, 3):
        try:
            contents = _build_contents(history)

            if tool_data:
                contents.append(
                    types.Content(
                        role="user",
                        parts=[types.Part(text=(
                            f"Os dados reais já foram obtidos pela ferramenta: {tool_data}. "
                            f"Use ESSES dados para responder ao usuário. "
                            f"Não invente nada além do que está aqui. "
                            f"Responda no formato JSON exato do sistema."
                        ))]
                    )
                )
            else:
                contents.append(
                    types.Content(
                        role="user",
                        parts=[types.Part(text=(
                            "A ferramenta não conseguiu obter dados reais agora. "
                            "Informe ao usuário que a informação está indisponível no momento. "
                            "NUNCA invente valores, preços ou percentuais financeiros. "
                            "Responda no formato JSON exato do sistema."
                        ))]
                    )
                )

            config = types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.7,
                tools=None,
            )

            print(f"[RETRY {retry_attempt}] Chamando Gemini sem tools...", flush=True)
            response = client.models.generate_content(
                model=MODEL_DEFAULT,
                config=config,
                contents=contents
            )

            if response and response.text and response.text.strip():
                print(f"[RETRY {retry_attempt}] ✓ Sucesso!", flush=True)
                raw = response.text
                parsed = parse_response(raw, character_name)
                if parsed and parsed[0].get("text", "").strip():
                    return parsed

            print(f"[RETRY {retry_attempt}] Ainda vazio, tentando novamente...", flush=True)
        except Exception as e:
            print(f"[RETRY {retry_attempt}] Erro: {str(e)[:50]}", flush=True)
            continue

    print(f"[RETRY] Todos os retries falharam, usando fallback", flush=True)
    return [_make_fallback(character_name, "Desculpe, não consegui processar sua pergunta agora. Tente novamente.")]


def _extract_tool_results(response) -> list[types.Part]:
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
_history_file_lock = threading.Lock()


def normalize_character_name(character_name: str) -> str:
    return character_name.lower().replace(" ", "_")


def load_history(character_name: str) -> list:
    key = normalize_character_name(character_name)
    with _history_file_lock:
        if key in _history_cache and HISTORY_FILE.exists():
            return list(_history_cache[key])

        if not HISTORY_FILE.exists():
            _history_cache[key] = []
            return []

        try:
            content = HISTORY_FILE.read_text(encoding="utf-8")
            if not content:
                _history_cache[key] = []
                return []
            data = json.loads(content)
            if not isinstance(data, dict):
                _history_cache[key] = []
                return []
            history = data.get(key, [])
            _history_cache[key] = history
            return list(history)
        except json.JSONDecodeError:
            _history_cache[key] = []
            return []


def persist_history(character_name: str, history: list) -> None:
    key = normalize_character_name(character_name)
    trimmed = history[-MAX_HISTORY:]
    with _history_file_lock:
        _history_cache[key] = trimmed
        all_history: dict = {}
        if HISTORY_FILE.exists():
            try:
                content = HISTORY_FILE.read_text(encoding="utf-8")
                if content:
                    all_history = json.loads(content)
            except json.JSONDecodeError:
                all_history = {}
        all_history[key] = trimmed
        HISTORY_FILE.write_text(
            json.dumps(all_history, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def clear_history(character_name: str) -> bool:
    key = normalize_character_name(character_name)
    with _history_file_lock:
        if not HISTORY_FILE.exists():
            _history_cache.pop(key, None)
            return False

        try:
            content = HISTORY_FILE.read_text(encoding="utf-8")
            if not content:
                _history_cache.pop(key, None)
                return False
            all_history = json.loads(content)
        except json.JSONDecodeError:
            _history_cache.pop(key, None)
            return False

        if key not in all_history:
            _history_cache.pop(key, None)
            return False

        del all_history[key]
        _history_cache.pop(key, None)
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
                temperature=0.5,
            ),
            contents=contents,
        )
        return response.text or ""
    except Exception:
        logger.exception("call_api falhou para %s", character_name)
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
    print(f"[GENERATE] Iniciando para {character_name}: '{message[:50]}'", flush=True)

    try:
        character = load_character(character_name)
    except FileNotFoundError:
        print(f"[GENERATE] ✗ Personagem não encontrado: {character_name}", flush=True)
        raise

    history = load_history(character_name)
    fn_tools, search_tools = build_tools_for_character(character)

    print(f"[GENERATE] Model: {MODEL_DEFAULT}, FnTools: {1 if fn_tools else 0}, SearchTools: {1 if search_tools else 0}, History: {len(history)}", flush=True)

    history.append({"role": Role.USER, "content": message})
    contents = _build_contents(history)
    phase2_contents = list(contents)  # snapshot limpo para fase 2 (antes da fase 1 modificar)
    system_prompt = build_system_prompt(character_name, character)

    # ── fase 1: function tools ────────────────────────────
    max_iterations = 5
    raw = None
    response = None

    for iteration in range(1, max_iterations + 1):
        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.5,
            tools=fn_tools or [],
        )

        try:
            print(f"[LOOP {iteration}] Chamando Gemini...", flush=True)
            response = client.models.generate_content(
                model=MODEL_DEFAULT,
                config=config,
                contents=contents
            )
            print(f"[LOOP {iteration}] ✓ Response OK", flush=True)
            _log_grounding_if_used(response)
        except Exception as e:
            error_text = str(e)[:50]
            print(f"[LOOP {iteration}] ✗ Erro: {error_text}", flush=True)
            if iteration == 1:
                return [_make_fallback(character_name, f"Erro API: {error_text}")]
            else:
                if iteration < max_iterations:
                    continue
                break

        if not response or not response.candidates:
            print(f"[LOOP {iteration}] ✗ Response vazio", flush=True)
            if iteration < max_iterations:
                continue
            raw = None
            break

        if not _has_tool_call(response):
            raw = response.text
            print(f"[LOOP {iteration}] ✓ Resposta final", flush=True)
            break

        tool_results = _extract_tool_results(response)

        if not tool_results:
            raw = response.text
            print(f"[LOOP {iteration}] ✓ Saiu (sem tool results)", flush=True)
            break

        if response.candidates[0].content:
            contents.append(response.candidates[0].content)

        contents.append(
            types.Content(role="tool", parts=tool_results)
        )
        print(f"[LOOP {iteration}] → Continuando com mais uma iteração...", flush=True)

    if raw is None and response:
        raw = response.text
    # ── fim da fase 1 ────────────────────────────────────

    # ── fase 2: google_search (se nenhuma fn tool foi usada) ──
    fn_tools_used = any(getattr(c, "role", None) == "tool" for c in contents)
    if search_tools and (not fn_tools_used or not (raw and raw.strip())):
        print(f"[PHASE2] Tentando google_search...", flush=True)
        try:
            config2 = types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.5,
                tools=search_tools,
            )
            response2 = client.models.generate_content(
                model=MODEL_SEARCH,
                config=config2,
                contents=phase2_contents,
            )
            _log_grounding_if_used(response2)
            if response2 and response2.text and response2.text.strip():
                raw = response2.text
                print(f"[PHASE2] ✓ Resultado via google_search", flush=True)
        except Exception:
            logger.exception("[PHASE2] google_search falhou para %s", character_name)
    # ── fim da fase 2 ────────────────────────────────────

    print(f"[PARSE] Raw: '{str(raw)[:80] if raw else 'VAZIO'}'", flush=True)

    parsed = parse_response(raw or "", character_name)

    # Se ficou vazio, tenta retry — passando dados reais das tools se existirem
    if not parsed or not parsed[0].get("text", "").strip():
        print(f"[RETRY] Resposta vazia! Tentando retry sem tools...", flush=True)
        tool_data = _extract_tool_data(contents)
        if tool_data:
            print(f"[RETRY] Dado real encontrado nas tools, passando para retry...", flush=True)
        else:
            print(f"[RETRY] Sem dado real disponível.", flush=True)
        parsed = _retry_simple_response(
            character_name, character, history, system_prompt,
            tool_data=tool_data
        )

    print(f"[PARSE] Resultado final: '{parsed[0]['text'][:60]}'", flush=True)

    try:
        history.append({"role": Role.MODEL, "content": parsed[0]["text"]})
        persist_history(character_name, history)
    except Exception:
        logger.exception("Erro ao salvar histórico para %s", character_name)

    return parsed


# ======================================================
# DEBUG
# ======================================================
if __name__ == "__main__":
    print(generate_message("Qual a Selic hoje?", "Corretor Rodrigo"))
