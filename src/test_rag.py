from retrieve import search, rerank_results, build_context, build_sources, process_query
from prompt import build_rag_prompt
from generate import generate_answer


query = input("Ask a Visa dispute question: ")

query = process_query(query)

results = search(query, n_results=5)
results = rerank_results(query, results)

context = build_context(results)

sources = build_sources(results)

prompt = build_rag_prompt(query, context)

answer = generate_answer(prompt)

print("\n" + "=" * 80)
print("RAG ANSWER")
print("=" * 80)
print(answer)

print("\n" + "-" * 80)
print("SOURCES")
print("-" * 80)

for source in sources:
    print(
        f"- Condition {source['condition']} — "
        f"{source['title']} — "
        f"Printed Page {source['pages']}"
    )