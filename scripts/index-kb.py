#!/opt/homebrew/bin/python3
"""
HaMm3r OS — Knowledge Base Indexer
Indexes ~/HaMm3r-KB into Chroma vector DB for semantic search / RAG
Run manually or add to cron for auto-indexing
"""

import sys
import os
import hashlib
from pathlib import Path
from datetime import datetime

# Point at open-webui's venv chroma
VENV_SITE = Path.home() / "open-webui/.venv/lib/python3.11/site-packages"
sys.path.insert(0, str(VENV_SITE))

import chromadb

KB = Path.home() / "HaMm3r-KB"
CHROMA_PATH = Path.home() / "open-webui/data/vector_db"
COLLECTION_NAME = "hammer_kb"

# File types to index
EXTENSIONS = [".md", ".txt", ".csv", ".json"]

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Split text into overlapping chunks for better retrieval."""
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks if chunks else [text]

def file_hash(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()

def index_kb():
    print(f"[{datetime.now():%H:%M:%S}] 🔨 HaMm3r KB Indexer starting...")
    
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    
    # Get or create HaMm3r collection
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )
    
    existing = set(collection.get()["ids"]) if collection.count() > 0 else set()
    print(f"  Existing indexed chunks: {len(existing)}")
    
    indexed = 0
    skipped = 0
    
    for ext in EXTENSIONS:
        for fpath in KB.rglob(f"*{ext}"):
            # Skip system/hidden files
            if any(part.startswith(".") for part in fpath.parts):
                continue
            if "Drive-Sync" in str(fpath):
                continue  # Skip Drive-Sync duplicates
                
            try:
                text = fpath.read_text(encoding="utf-8", errors="ignore").strip()
                if not text or len(text) < 50:
                    continue
                    
                fhash = file_hash(fpath)
                rel_path = str(fpath.relative_to(Path.home()))
                
                # Check if already indexed (same hash)
                chunk_id_base = f"{rel_path}_{fhash}"
                if any(chunk_id_base in eid for eid in existing):
                    skipped += 1
                    continue
                
                # Chunk the document
                chunks = chunk_text(text)
                
                ids = [f"{chunk_id_base}_chunk{i}" for i in range(len(chunks))]
                metadatas = [{
                    "source": rel_path,
                    "filename": fpath.name,
                    "category": fpath.parent.name,
                    "hash": fhash,
                    "chunk": i,
                    "total_chunks": len(chunks)
                } for i in range(len(chunks))]
                
                collection.add(
                    documents=chunks,
                    ids=ids,
                    metadatas=metadatas
                )
                
                indexed += len(chunks)
                print(f"  ✓ {rel_path} ({len(chunks)} chunks)")
                
            except Exception as e:
                print(f"  ✗ {fpath.name}: {e}")
    
    total = collection.count()
    print(f"\n✅ Done — {indexed} new chunks indexed, {skipped} files skipped (unchanged)")
    print(f"   Total in HaMm3r KB collection: {total} chunks")
    print(f"   Collection: '{COLLECTION_NAME}' in {CHROMA_PATH}")
    return indexed, total

def search_kb(query: str, n_results: int = 5):
    """Quick search test."""
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    try:
        collection = client.get_collection(COLLECTION_NAME)
    except Exception:
        print("No HaMm3r KB collection found — run indexer first")
        return
    
    results = collection.query(query_texts=[query], n_results=n_results)
    
    print(f"\n🔍 Search: '{query}'\n")
    for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0]), 1):
        print(f"--- Result {i} [{meta['filename']}] ---")
        print(doc[:300])
        print()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "search":
        query = " ".join(sys.argv[2:]) or "investment strategy"
        search_kb(query)
    else:
        indexed, total = index_kb()
        
        # Quick search test after indexing
        if total > 0:
            print("\n--- Test search: 'VA disability' ---")
            search_kb("VA disability rating", n_results=2)
