"""Clean, callable entry point for the existing Visa dispute RAG pipeline.

This module does NOT reimplement retrieval, reranking, prompting, or
generation. It only orchestrates the existing building blocks that already
live in retrieve.py, prompt.py and generate.py so that other layers (e.g. a
FastAPI app) can call a single function instead of wiring the pipeline steps
themselves.
"""

import sys
from pathlib import Path

# retrieve.py / prompt.py / generate.py import each other using bare module
# names (e.g. `from retrieve import search`), so this directory must be on
# sys.path regardless of who imports rag_pipeline (script, pytest, FastAPI).
_SRC_DIR = Path(__file__).resolve().parent
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from retrieve import (  # noqa: E402
    build_context,
    build_sources,
    process_query,
    rerank_results,
    search,
)
from prompt import build_rag_prompt  # noqa: E402
from generate import generate_answer  # noqa: E402

DEFAULT_N_RESULTS = 5


def ask_question(question: str, n_results: int = DEFAULT_N_RESULTS) -> dict:
    """Run the full RAG pipeline for a single question.

    Args:
        question: The raw user question.
        n_results: Number of chunks to retrieve from ChromaDB before
            reranking.

    Returns:
        A dict with keys:
            - "answer": the generated answer (str)
            - "sources": list of source dicts (condition/title/pages)

    Raises:
        ValueError: If the question is empty/blank after stripping.
    """
    query = process_query(question)

    results = search(query, n_results=n_results)
    results = rerank_results(query, results)

    context = build_context(results)
    sources = build_sources(results)

    prompt = build_rag_prompt(query, context)
    answer = generate_answer(prompt)

    return {"answer": answer, "sources": sources}
