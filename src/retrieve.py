import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "visa_disputes"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def search(query, n_results=5):
    model = SentenceTransformer(EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_collection(COLLECTION_NAME)

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True,
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
    )

    return results

def rerank_results(query, results):
    """Rerank retrieved chunks using simple keyword overlap."""

    query_words = set(query.lower().split())

    scored = []

    for i in range(len(results["documents"][0])):
        metadata = results["metadatas"][0][i]

        title = metadata.get("title", "")
        condition = metadata.get("condition", "")

        source_text = f"{title} {condition}".lower()
        source_words = set(source_text.split())

        keyword_score = len(query_words & source_words)

        scored.append((keyword_score, i))

    # Higher keyword score first
    scored.sort(reverse=True)

    reranked = {
        "documents": [[results["documents"][0][i] for _, i in scored]],
        "metadatas": [[results["metadatas"][0][i] for _, i in scored]],
        "distances": [[results["distances"][0][i] for _, i in scored]],
    }

    return reranked

def build_context(results):
    """Convert retrieved ChromaDB results into clean LLM context."""

    context_parts = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i, document in enumerate(documents):
        metadata = metadatas[i]
        distance = distances[i]

        condition = metadata.get("condition", "N/A")
        title = metadata.get("title", "N/A")
        subsection = metadata.get("subsection", "N/A")
        pages = metadata.get("printed_pages", "N/A")

        source = f"""
SOURCE {i + 1}
Condition: {condition}
Title: {title}
Subsection: {subsection}
Printed page(s): {pages}
Similarity distance: {distance:.4f}

Visa Evidence:
{document}
"""

        context_parts.append(source.strip())

    return "\n\n" + "\n\n".join(context_parts)

def build_sources(results):
    """Extract unique source information from retrieved results."""

    sources = []
    seen = set()

    for metadata in results["metadatas"][0]:
        condition = metadata.get("condition", "N/A")
        title = metadata.get("title", "N/A")
        pages = metadata.get("printed_pages", "N/A")

        source_key = (condition, title, pages)

        if source_key not in seen:
            sources.append({
                "condition": condition,
                "title": title,
                "pages": pages,
            })
            seen.add(source_key)

    return sources

def process_query(query):
    """Prepare a user query for retrieval."""
    query = query.strip()

    if not query:
        raise ValueError("Query cannot be empty.")

    return query


if __name__ == "__main__":
    user_query = input("Ask a Visa dispute question: ")

    query = process_query(user_query)
    results = search(query)

    for i, document in enumerate(results["documents"][0]):
        metadata = results["metadatas"][0][i]
        distance = results["distances"][0][i]

        print("\n" + "=" * 70)
        print(f"Result {i + 1} | distance: {distance:.4f}")
        print(
            f"Condition: {metadata.get('condition', '')} | "
            f"Title: {metadata.get('title', '')}"
        )
        print(f"Subsection: {metadata.get('subsection', '')}")
        print(f"Printed page(s): {metadata.get('printed_pages', '')}")
        print("-" * 70)
        print(document[:1500])