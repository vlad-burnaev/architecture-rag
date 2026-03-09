#!/usr/bin/env python3
"""
Demo script for RAG bot - shows retrieval and prompt construction
Can work without LLM API key to demonstrate the RAG pipeline
Supports: YandexGPT, Google Gemini, OpenAI
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag_bot import EternumNexusRAG


def demo_retrieval():
    """Demonstrate context retrieval without LLM."""
    print("\n" + "="*70)
    print("DEMO 1: Context Retrieval (No LLM required)")
    print("="*70 + "\n")
    
    bot = EternumNexusRAG()
    
    test_queries = [
        "What are the playable races?",
        "How does Stellarium currency work?",
        "Tell me about Terragorax",
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 70)
        
        context = bot.retrieve_context(query, k=3)
        
        print(f"\nRetrieved {len(context)} relevant documents:\n")
        for i, doc in enumerate(context, 1):
            print(f"[{i}] Source: {doc['source']}")
            print(f"    Preview: {doc['content'][:150]}...")
            print()
        
        input("Press Enter to continue...")


def demo_prompt_building():
    """Demonstrate prompt construction with Few-shot and CoT."""
    print("\n" + "="*70)
    print("DEMO 2: Prompt Building (Few-shot + Chain-of-Thought)")
    print("="*70 + "\n")
    
    bot = EternumNexusRAG()
    
    query = "What races can I play as?"
    print(f"Query: {query}\n")
    
    # Retrieve context
    context = bot.retrieve_context(query, k=2)
    
    # Build prompt
    prompt = bot.build_prompt(query, context)
    
    print("Generated Prompt:")
    print("="*70)
    print(prompt)
    print("="*70)
    
    print("\n\nKey components in the prompt:")
    print("  1. System instructions (use only context, think step-by-step)")
    print("  2. Few-shot examples (2 examples with reasoning)")
    print("  3. Retrieved context (relevant documents)")
    print("  4. User query")
    print("  5. CoT format (Reasoning → Answer)")


def demo_with_llm():
    """Demonstrate full RAG pipeline with LLM (if API key available)."""
    print("\n" + "="*70)
    print("DEMO 3: Full RAG Pipeline (Requires API Key)")
    print("="*70 + "\n")
    
    # Check for any available API key
    yandex_key = os.getenv("YANDEX_API_KEY")
    yandex_folder = os.getenv("YANDEX_FOLDER_ID")
    google_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not any([yandex_key and yandex_folder, google_key, openai_key]):
        print("No API key found - skipping LLM demo")
        print("\nTo test with LLM, set one of:")
        print("  YandexGPT: export YANDEX_API_KEY='key' && export YANDEX_FOLDER_ID='id'")
        print("  Gemini:    export GOOGLE_API_KEY='key'")
        print("  OpenAI:    export OPENAI_API_KEY='key'")
        print("\nThen run: make demo-bot")
        return
    
    print("API key found! Running full RAG pipeline...\n")
    
    bot = EternumNexusRAG()
    
    test_queries = [
        "What are the main playable races?",
        "How do I earn Stellarium currency?",
        "What is special about the Edgeblade race?",
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*70}")
        print(f"Test Query {i}: {query}")
        print('='*70)
        
        result = bot.query(query, k=3, verbose=True)
        
        print(f"\n{'='*70}")
        print("FINAL RESPONSE:")
        print('='*70)
        print(result['response'])
        print('='*70)
        
        if i < len(test_queries):
            input("\nPress Enter for next query...")


def main():
    """Main demo execution."""
    print("\n" + "="*70)
    print(" Eternum Nexus RAG Bot - Demonstration")
    print("="*70)
    print("\nThis demo shows the RAG pipeline components:")
    print("  1. Context Retrieval from Vector DB")
    print("  2. Prompt Construction (Few-shot + Chain-of-Thought)")
    print("  3. Full Pipeline with LLM (if API key available)")
    print("\n" + "="*70)
    
    while True:
        print("\n\nSelect demo:")
        print("  1 - Context Retrieval (works without API key)")
        print("  2 - Prompt Building (works without API key)")
        print("  3 - Full RAG Pipeline (requires OPENAI_API_KEY)")
        print("  0 - Exit")
        print()
        
        choice = input("Choice >>> ").strip()
        
        if choice == '1':
            demo_retrieval()
        elif choice == '2':
            demo_prompt_building()
        elif choice == '3':
            demo_with_llm()
        elif choice == '0':
            print("\nExiting demo...")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
