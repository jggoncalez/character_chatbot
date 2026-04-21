#!/usr/bin/env python3
"""Simula o comportamento da API com threading"""
import sys
sys.path.insert(0, '/home/racer/Codes/character_chatbot/backend')

from concurrent.futures import ThreadPoolExecutor
import time
from core.chat.pipeline import generate_message

def test_with_threadpool():
    """Simula a chamada com run_in_threadpool (como faz a API)"""
    print("\n=== Teste 1: Direct call (como no test_debug.py) ===")
    start = time.time()
    result = generate_message("Olá!", "Tux")
    elapsed = time.time() - start
    print(f"Result: {result[0]['text'][:60]}")
    print(f"Time: {elapsed:.2f}s\n")

    print("=== Teste 2: Via ThreadPoolExecutor (como faz a API) ===")
    with ThreadPoolExecutor(max_workers=1) as executor:
        start = time.time()
        future = executor.submit(generate_message, "Como você está?", "Tux")
        result = future.result(timeout=30)  # Timeout de 30s
        elapsed = time.time() - start
        print(f"Result: {result[0]['text'][:60]}")
        print(f"Time: {elapsed:.2f}s\n")

    print("=== Teste 3: Com Corretor/Selic (tem tool) ===")
    with ThreadPoolExecutor(max_workers=1) as executor:
        start = time.time()
        future = executor.submit(generate_message, "Qual a Selic hoje?", "Corretor Rodrigo")
        result = future.result(timeout=30)
        elapsed = time.time() - start
        print(f"Result: {result[0]['text'][:60]}")
        print(f"Time: {elapsed:.2f}s\n")

if __name__ == "__main__":
    test_with_threadpool()
