import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = BASE_DIR/"data"/"visa_dispute_chunks.json"
CHROMA_DIR = BASE_DIR / "chroma_db"

COLLECTION_NAME = "visa_disputes"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"Loaded {len(chunks)} chunks.")

    model = SentenceTransformer(EMBEDDING_MODEL)

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # Re-running ingestion should not create duplicates.
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "Visa Dispute Management Guidelines knowledge base"},
    )

    documents = [c["content"] for c in chunks]
    ids = [c["id"] for c in chunks]

    # Chroma metadata values should be scalar types, so page lists are stored as strings.
    metadatas = []
    for c in chunks:
        metadatas.append({
            "source": c["source"],
            "document_version": c["document_version"],
            "section": c["section"],
            "condition": c["condition"] or "",
            "title": c["title"],
            "subsection": c["subsection"],
            "pdf_pages": ",".join(map(str, c["pdf_pages"])),
            "printed_pages": ",".join(map(str, c["printed_pages"])),
        })

    print("Creating embeddings...")
    embeddings = model.encode(
        documents,
        normalize_embeddings=True,
        show_progress_bar=True,
    ).tolist()

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"\nDone! Stored {collection.count()} chunks in ChromaDB.")
    print(f"Database: {CHROMA_DIR}")


if __name__ == "__main__":
    main()
