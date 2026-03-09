#!/usr/bin/env python3
"""
Vector Index Builder for Eternum Nexus Knowledge Base
Creates embeddings and indexes documents in ChromaDB
"""

import os
import time
from pathlib import Path
from typing import List, Dict

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Document class
class Document:
    def __init__(self, page_content: str, metadata: dict = None):
        self.page_content = page_content
        self.metadata = metadata or {}


def load_documents(knowledge_base_dir: str = "knowledge_base") -> List[Document]:
    """Load all text documents from knowledge base directory."""
    documents = []
    kb_path = Path(knowledge_base_dir)
    
    print(f"Loading documents from: {kb_path}")
    
    for txt_file in sorted(kb_path.glob("*.txt")):
        print(f"  Loading: {txt_file.name}")
        
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create document with metadata
        doc = Document(
            page_content=content,
            metadata={
                "source": txt_file.name,
                "file_path": str(txt_file),
                "doc_id": txt_file.stem
            }
        )
        documents.append(doc)
    
    print(f"\nLoaded {len(documents)} documents")
    return documents


def split_documents(documents: List[Document], 
                   chunk_size: int = 500,
                   chunk_overlap: int = 50) -> List[Document]:
    """Split documents into chunks for embedding."""
    print(f"\nSplitting documents into chunks...")
    print(f"  Chunk size: {chunk_size} characters")
    print(f"  Chunk overlap: {chunk_overlap} characters")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    
    # Add chunk metadata
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i
        chunk.metadata["chunk_length"] = len(chunk.page_content)
    
    print(f"Created {len(chunks)} chunks")
    return chunks


def create_embeddings_model(model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    """Initialize the embeddings model."""
    print(f"\nInitializing embeddings model: {model_name}")
    
    # Use local cache directory in project
    cache_dir = "./models_cache"
    os.makedirs(cache_dir, exist_ok=True)
    
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True},
        cache_folder=cache_dir
    )
    
    print("  Model loaded successfully")
    return embeddings


def build_vector_index(chunks: List[Document], 
                      embeddings,
                      persist_directory: str = "chroma_db"):
    """Build ChromaDB vector index from chunks."""
    print(f"\nBuilding vector index...")
    print(f"  Persist directory: {persist_directory}")
    print(f"  Number of chunks to index: {len(chunks)}")
    
    start_time = time.time()
    
    # Create ChromaDB vector store
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name="eternum_nexus_kb"
    )
    
    elapsed_time = time.time() - start_time
    
    print(f"\n  Indexing completed in {elapsed_time:.2f} seconds")
    print(f"  Average: {elapsed_time/len(chunks):.3f} seconds per chunk")
    
    return vectorstore


def test_search(vectorstore, queries: List[str], k: int = 3):
    """Test vector search with sample queries."""
    print("\n" + "="*60)
    print("Testing Vector Search")
    print("="*60)
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        print("-" * 60)
        
        results = vectorstore.similarity_search(query, k=k)
        
        for i, doc in enumerate(results, 1):
            print(f"\nResult {i}:")
            print(f"  Source: {doc.metadata.get('source', 'unknown')}")
            print(f"  Chunk ID: {doc.metadata.get('chunk_id', 'unknown')}")
            print(f"  Content preview: {doc.page_content[:150]}...")


def get_index_stats(vectorstore) -> Dict:
    """Get statistics about the vector index."""
    collection = vectorstore._collection
    
    stats = {
        "total_chunks": collection.count(),
        "collection_name": collection.name,
    }
    
    return stats


def main():
    """Main execution function."""
    print("="*60)
    print("Vector Index Builder - Eternum Nexus Knowledge Base")
    print("="*60)
    print()
    
    # Configuration
    KNOWLEDGE_BASE_DIR = "knowledge_base"
    PERSIST_DIR = "chroma_db"
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Step 1: Load documents
    documents = load_documents(KNOWLEDGE_BASE_DIR)
    
    # Step 2: Split into chunks
    chunks = split_documents(documents, CHUNK_SIZE, CHUNK_OVERLAP)
    
    # Step 3: Initialize embeddings model
    embeddings = create_embeddings_model(MODEL_NAME)
    
    # Step 4: Build vector index
    vectorstore = build_vector_index(chunks, embeddings, PERSIST_DIR)
    
    # Step 5: Get statistics
    stats = get_index_stats(vectorstore)
    
    print("\n" + "="*60)
    print("Index Statistics")
    print("="*60)
    print(f"Total documents: {len(documents)}")
    print(f"Total chunks: {stats['total_chunks']}")
    print(f"Collection name: {stats['collection_name']}")
    print(f"Embedding model: {MODEL_NAME}")
    print(f"Embedding dimension: 384")
    print(f"Chunk size: {CHUNK_SIZE} characters")
    print(f"Chunk overlap: {CHUNK_OVERLAP} characters")
    print()
    
    # Step 6: Test with sample queries
    test_queries = [
        "What are the main races in Eternum Nexus?",
        "How does the Stellarium currency system work?",
        "Tell me about Terragorax the dragon boss"
    ]
    
    test_search(vectorstore, test_queries, k=3)
    
    print("\n" + "="*60)
    print("Index building completed successfully!")
    print(f"Vector database saved to: {PERSIST_DIR}/")
    print("="*60)


if __name__ == "__main__":
    main()
