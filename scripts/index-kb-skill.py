#!/home/user/open-webui/.venv/bin/python3
"""
HaMm3r OS — Knowledge Base Indexer
Index ~/HaMm3r-KB into Chroma vector DB for semantic search / RAG.

IMPORTANT: Run with ~/open-webui/.venv/bin/python3 — NOT homebrew or system python.
Chroma uses numpy C extensions compiled for Python 3.11.

Usage:
  ~/open-webui/.venv/bin/python3 index-kb.py          # index all files
  ~/open-webui/.venv/bin/python3 index-kb.py search "VA disability"  # test search
"""

import sys
import os
import hashlib
from pathlib import Path
from datetime import datetime

import chromadb

KB = Path.home() / "HaMm3r-KB"
CHROMA_PATH = Path.home() / "open-webui/data/vector_db"
COLLECTION_NAME = "hammer_kb"
EXTENSIONS = [".md", ".txt", ".csv", ".json"]


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
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
    print(f"[{datetime.now():%H:%M:%S}] HaMm3r KB Indexer starting...")
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )
    existing = set(collection.get()["ids"]) if collection.count() > 0 else set()
    print(f"  Existing chunks: {len(existing)}")

    indexed = 0
    skipped = 0

    for ext in EXTENSIONS:
        for fpath in KB.rglob(f"*{ext}"):
            if any(part.startswith(".") for part in fpath.parts):
                continue
            if "Drive-Sync" in str(fpath):
                continue
            try:
                text = fpath.read_text(encoding="utf-8", errors="ignore").strip()
                if not text or len(text) < 50:
                    continue
                fhash = file_hash(fpath)
                rel_path = str(fpath.relative_to(Path.home()))
                chunk_id_base = f"{rel_path}_{fhash}"
                if any(chunk_id_base in eid for eid in existing):
                    skipped += 1
                    continue
                chunks = chunk_text(text)
                ids = [f"{chunk_id_base}_chunk{i}" for i in range(len(chunks))]
                metadatas = [{
                    "source": rel_path, "filename": fpath.name,
                    "category": fpath.parent.name, "hash": fhash,
                    "chunk": i, "total_chunks": len(chunks)
                } for i in range(len(chunks))]
                collection.add(documents=chunks, ids=ids, metadatas=metadatas)
                indexed += len(chunks)
                print(f"  + {fpath.name} ({len(chunks)} chunks)")
            except Exception as e:
                print(f"  ERROR {fpath.name}: {e}")

    total = collection.count()
    print(f"\nDone — {indexed} new chunks, {skipped} unchanged, {total} total")
    return indexed, total


def search_kb(query: str, n_results: int = 5):
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    try:
        collection = client.get_collection(COLLECTION_NAME)
    except Exception:
        print("No hammer_kb collection — run indexer first")
        return
    results = collection.query(query_texts=[query], n_results=n_results)
    print(f"\nSearch: '{query}'\n")
    for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0]), 1):
        print(f"--- Result {i} [{meta['filename']}] ---")
        print(doc[:300])
        print()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "search":
        search_kb(" ".join(sys.argv[2:]) or "investment strategy")
    else:
        index_kb()
