#!/usr/bin/env python3
"""Test data/hora com ferramenta"""
import sys
sys.path.insert(0, '/home/racer/Codes/character_chatbot/backend')

from core.chat.pipeline import generate_message

print("Test 1: Pergunta sobre hora")
result = generate_message("Que horas são agora?", "Tux")
print(f"Resposta: {result[0]['text']}\n")

print("Test 2: Pergunta sobre data")
result = generate_message("Que dia é hoje?", "Tux")
print(f"Resposta: {result[0]['text']}\n")

print("Test 3: Pergunta sobre clima")
result = generate_message("Como está o clima em São Paulo?", "Tux")
print(f"Resposta: {result[0]['text']}\n")

print("Test 4: Pergunta normal (não tool)")
result = generate_message("Olá, tudo bem?", "Tux")
print(f"Resposta: {result[0]['text']}\n")
