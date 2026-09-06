from retrieve import search, build_context, build_sources, process_query
from prompt import build_rag_prompt
from generate import generate_answer


TEST_QUERIES = [
    "Customer says they never received the merchandise. What evidence can the merchant provide?",
    "The customer says they paid using another payment method. What should the merchant do?",
    "What evidence can support a card-absent fraud dispute?",
    "Customer was charged twice for the same transaction. What should the merchant do?",
    "What should a merchant do when a customer disputes a transaction?"
]


for i, query in enumerate(TEST_QUERIES, start=1):

    print("\n" + "=" * 80)
    print(f"TEST {i}")
    print("=" * 80)
    print(f"QUESTION: {query}")

    query = process_query(query)

    results = search(query, n_results=5)

    context = build_context(results)

    sources = build_sources(results)

    prompt = build_rag_prompt(query, context)

    answer = generate_answer(prompt)

    print("\nANSWER:")
    print(answer)

    print("\nSOURCES:")
    for source in sources:
        print(
            f"- Condition {source['condition']} — "
            f"{source['title']} — "
            f"Printed Page {source['pages']}"
        )