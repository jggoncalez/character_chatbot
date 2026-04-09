#!/usr/bin/env python3
"""Test parsing de respostas"""
import sys
sys.path.insert(0, '/home/racer/Codes/character_chatbot/backend')

from core.chat.pipeline import parse_response, clean_json

test_cases = [
    # (input, expected_has_text, description)
    ('{"character": "Tux", "text": "Olá!", "state": "happy"}', True, "Dict único"),
    ('[{"character": "Tux", "text": "Olá!", "state": "happy"}]', True, "Array com dict"),
    ('```json\n{"character": "Tux", "text": "Teste", "state": "neutral"}\n```', True, "JSON com markdown backticks"),
    ('', False, "String vazia"),
    ('   ', False, "Só whitespace"),
    ('[{"text": "resposta"}]', True, "Sem fields opcionais"),
    ('Resposta de texto puro', True, "Fallback para texto"),
]

print("Testando parse_response:\n")
for test_input, should_have_text, description in test_cases:
    try:
        result = parse_response(test_input, "Tux")
        has_text = result and result[0].get("text") and result[0]["text"] != "..."

        status = "✓" if has_text == should_have_text else "✗"
        print(f"{status} {description}")
        print(f"  Input: {repr(test_input[:50])}")
        print(f"  Output: {result[0] if result else 'VAZIO'}")
        print()
    except Exception as e:
        print(f"✗ {description} - ERRO: {e}")
        print()
