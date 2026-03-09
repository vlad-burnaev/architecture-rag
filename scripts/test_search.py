#!/usr/bin/env python3
"""
Test script for vector search in Eternum Nexus Knowledge Base
Run queries against the existing ChromaDB index
"""

import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


def load_vectorstore():
    """Load existing ChromaDB vector store."""
    print("Loading vector index...")
    
    # Use local cache directory
    cache_dir = "./models_cache"
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True},
        cache_folder=cache_dir
    )
    
    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings,
        collection_name="eternum_nexus_kb"
    )
    
    print(f"Index loaded: {vectorstore._collection.count()} chunks\n")
    return vectorstore


def search(vectorstore, query: str, k: int = 5, show_content: bool = True):
    """Perform similarity search and display results."""
    print("=" * 70)
    print(f"QUERY: {query}")
    print("=" * 70)
    
    results = vectorstore.similarity_search(query, k=k)
    
    for i, doc in enumerate(results, 1):
        print(f"\n[Результат {i}]")
        print(f"  Файл: {doc.metadata.get('source', 'unknown')}")
        print(f"  Chunk ID: {doc.metadata.get('chunk_id', 'unknown')}")
        
        if show_content:
            content = doc.page_content
            # Show first 300 chars
            preview = content[:300] + "..." if len(content) > 300 else content
            print(f"  Содержимое:\n    {preview.replace(chr(10), chr(10) + '    ')}")
    
    print("\n" + "=" * 70 + "\n")


def interactive_mode(vectorstore):
    """Interactive query mode."""
    print("\n" + "=" * 70)
    print("ИНТЕРАКТИВНЫЙ РЕЖИМ ПОИСКА")
    print("=" * 70)
    print("Введите запрос (или 'exit' для выхода)")
    print("Команды:")
    print("  - Обычный запрос: просто введите текст")
    print("  - 'k=N': изменить количество результатов (например: k=10)")
    print("  - 'exit' или 'quit': выход")
    print("=" * 70 + "\n")
    
    k = 5  # default
    
    while True:
        query = input("Запрос >>> ").strip()
        
        if not query:
            continue
            
        if query.lower() in ['exit', 'quit', 'q']:
            print("Выход...")
            break
        
        # Check for k= command
        if query.startswith('k='):
            try:
                k = int(query.split('=')[1])
                print(f"Количество результатов изменено на: {k}\n")
                continue
            except:
                print("Ошибка: используйте формат k=5\n")
                continue
        
        search(vectorstore, query, k=k)


def main():
    """Main execution."""
    print("\n" + "=" * 70)
    print("Тестирование векторного поиска - Eternum Nexus")
    print("=" * 70 + "\n")
    
    # Load vector store
    vectorstore = load_vectorstore()
    
    # Predefined test queries
    test_queries = [
        "What are the main playable races?",
        "How does the currency system work?",
        "Tell me about Terragorax the dragon boss",
        "What is the Champion's Arena?",
        "How do I join a guild?",
        "What classes can Aetherians become?",
        "Explain the enhancement system",
        "Where is Valorheim Citadel located?"
    ]
    
    print("=" * 70)
    print("ПРЕДУСТАНОВЛЕННЫЕ ТЕСТОВЫЕ ЗАПРОСЫ")
    print("=" * 70)
    print("\nВыберите опцию:")
    print("  1 - Запустить все тестовые запросы")
    print("  2 - Выбрать конкретный запрос")
    print("  3 - Интерактивный режим (свои запросы)")
    print("  0 - Выход")
    print()
    
    choice = input("Выбор >>> ").strip()
    
    if choice == '1':
        # Run all test queries
        print("\n\nЗапуск всех тестовых запросов...\n")
        for query in test_queries:
            search(vectorstore, query, k=3, show_content=True)
            input("Нажмите Enter для следующего запроса...")
    
    elif choice == '2':
        # Choose specific query
        print("\nДоступные запросы:")
        for i, q in enumerate(test_queries, 1):
            print(f"  {i}. {q}")
        print()
        
        try:
            idx = int(input("Номер запроса >>> ").strip()) - 1
            if 0 <= idx < len(test_queries):
                query = test_queries[idx]
                k = int(input("Количество результатов (по умолчанию 5) >>> ").strip() or "5")
                search(vectorstore, query, k=k)
            else:
                print("Неверный номер")
        except:
            print("Ошибка ввода")
    
    elif choice == '3':
        # Interactive mode
        interactive_mode(vectorstore)
    
    else:
        print("Выход...")


if __name__ == "__main__":
    main()
