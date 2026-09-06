from retrieve import (
    process_query,
    search,
    rerank_results,
    build_context,
    build_sources,
)
from generate import generate_answer
from prompt import build_rag_prompt


def ask_question(question):
    """Run the complete RAG pipeline."""

    query = process_query(question)

    results = search(query)

    reranked_results = rerank_results(query, results)

    context = build_context(reranked_results)

    rag_prompt = build_rag_prompt(query, context)

    answer = generate_answer(rag_prompt)

    sources = build_sources(reranked_results)

    return {
        "answer": answer,
        "sources": sources,
    }