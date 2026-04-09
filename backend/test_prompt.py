#!/usr/bin/env python3
"""Teste rápido do system prompt"""
import sys
sys.path.insert(0, '/home/racer/Codes/character_chatbot/backend')

from core.chat.pipeline import (
    build_system_prompt, load_character, clear_history,
    generate_message
)

# Clear history
print("[SETUP] Limpando histórico...")
clear_history("Tux")
clear_history("Corretor Rodrigo")

# Carrega personagens
print("\n[PROMPT TEST] Verificando system prompts:\n")
for char_name in ["Tux", "Corretor Rodrigo"]:
    char = load_character(char_name)
    prompt = build_system_prompt(char_name, char)
    print(f"=== {char_name} ===")
    print(prompt[:200] + "...\n")

# Test simples
print("\n[TEST] Testando Tux com 'Olá!'")
try:
    result = generate_message("Olá!", "Tux")
    text = result[0].get("text", "[VAZIO]")
    print(f"✓ Resposta: {text}")
except Exception as e:
    print(f"✗ Erro: {e}")
