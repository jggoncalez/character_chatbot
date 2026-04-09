#!/usr/bin/env python3
"""Diagnóstico completo do chatbot"""
import sys
import os
sys.path.insert(0, '/home/racer/Codes/character_chatbot/backend')

from core.chat.pipeline import (
    generate_message, load_character, load_history,
    normalize_character_name, clear_history
)
import json

def test_full_flow():
    character = "Tux"
    message1 = "Olá, tudo bem?"
    message2 = "Como funciona o Linux?"
    message3 = "Explique mais sobre o kernel"

    print("="*70)
    print("TESTE COMPLETO DO CHATBOT")
    print("="*70)

    # Clear history
    print(f"\n[SETUP] Limpando histórico de {character}...")
    clear_history(character)

    # Load character
    print(f"[SETUP] Carregando personagem {character}...")
    try:
        char_data = load_character(character)
        print(f"  ✓ Nome: {char_data.get('name')}")
        print(f"  ✓ Tools: {char_data.get('tools', [])}")
    except Exception as e:
        print(f"  ✗ Erro: {e}")
        return

    # Test 1
    print(f"\n[TEST 1] Primeiro envio: '{message1}'")
    try:
        result1 = generate_message(message1, character)
        text1 = result1[0].get("text") if result1 else ""
        print(f"  Resposta: {text1}")
        if text1 and text1 != "...":
            print(f"  ✓ Sucesso!")
        else:
            print(f"  ✗ Resposta vazia ou fallback!")
    except Exception as e:
        print(f"  ✗ Erro: {e}")
        import traceback
        traceback.print_exc()

    # Check history
    print(f"\n[DEBUG] Histórico após TEST 1:")
    history = load_history(character)
    print(f"  Histórias salvas: {len(history)}")
    for i, h in enumerate(history[-2:]):
        print(f"    {i}: {h['role']} - {h['content'][:50]}")

    # Test 2
    print(f"\n[TEST 2] Segundo envio: '{message2}'")
    try:
        result2 = generate_message(message2, character)
        text2 = result2[0].get("text") if result2 else ""
        print(f"  Resposta: {text2}")
        if text2 and text2 != "...":
            print(f"  ✓ Sucesso!")
        else:
            print(f"  ✗ Resposta vazia ou fallback!")
    except Exception as e:
        print(f"  ✗ Erro: {e}")

    # Test 3
    print(f"\n[TEST 3] Terceiro envio: '{message3}'")
    try:
        result3 = generate_message(message3, character)
        text3 = result3[0].get("text") if result3 else ""
        print(f"  Resposta: {text3}")
        if text3 and text3 != "...":
            print(f"  ✓ Sucesso!")
        else:
            print(f"  ✗ Resposta vazia ou fallback!")
    except Exception as e:
        print(f"  ✗ Erro: {e}")

    # Final history
    print(f"\n[FINAL] Histórico completo:")
    history = load_history(character)
    print(f"  Total de mensagens: {len(history)}")
    for h in history:
        role = h['role'].upper()
        text = h['content'][:60].replace('\n', ' ')
        print(f"   {role}: {text}...")

if __name__ == "__main__":
    test_full_flow()
