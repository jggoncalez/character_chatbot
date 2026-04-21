#!/usr/bin/env python3
"""Testa o comportamento com retries quando vazio"""
import sys
sys.path.insert(0, '/home/racer/Codes/character_chatbot/backend')

from core.chat.pipeline import generate_message
import json

# Simula comportamento testando vários personagens e mensagens
print("=== Teste de Retry Mechanism ===\n")

tests = [
    ("Tux", "Olá!"),
    ("Tux", "Me fale sobre programação"),
    ("Corretor Rodrigo", "Qual a Selic?"),
    ("Corretor Rodrigo", "E qual o preço do dólar?"),
]

for char,msg in tests:
    print(f"\n{'='*60}")
    print(f"Character: {char}")
    print(f"Message: {msg}")
    print(f"{'='*60}")
    try:
        result = generate_message(msg, char)
        print(f"\n✓ Response: {result[0]['text'][:80]}")
    except Exception as e:
        print(f"\n✗ Error: {e}")
