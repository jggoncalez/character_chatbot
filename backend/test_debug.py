#!/usr/bin/env python3
"""Debug script para testar o pipeline do chatbot"""
import sys
import os
sys.path.insert(0, '/home/racer/Codes/character_chatbot/backend')

from core.chat.pipeline import generate_message
import json

def test_character(char_name: str, message: str):
    print(f"\n{'='*60}")
    print(f"Testando: {char_name}")
    print(f"Mensagem: {message}")
    print(f"{'='*60}")

    try:
        result = generate_message(message, char_name)
        print(f"\n✓ Resposta recebida!")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return True
    except Exception as e:
        print(f"\n✗ Erro: {type(e).__name__}")
        print(f"Detalhes: {str(e)[:200]}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Teste com um personagem simples
    print("[TEST 1/3] Teste com Tux (sem tools)")
    test_character("Tux", "Olá!")

    print("\n[TEST 2/3] Teste com Tux (segunda comunicação)")
    test_character("Tux", "Como você está?")

    print("\n[TEST 3/3] Teste com Corretor Rodrigo (com tools)")
    test_character("Corretor Rodrigo", "Qual a Selic hoje?")
