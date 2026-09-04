from retrieve import search, build_context
from prompt import build_rag_prompt


queries = [

    "Customer says they never received the merchandise. What evidence can the merchant provide?",

    "The customer says they paid using another payment method. What should the merchant do?",

    "What evidence can support a card-absent fraud dispute?",

]


for query in queries:

    print("\n\n" + "#" * 80)
    print("QUERY:", query)

    results = search(query, n_results=5)

    context = build_context(results)

    prompt = build_rag_prompt(query, context)

    print("\n" + "=" * 80)
    print("RAG PROMPT")
    print("=" * 80)
    print(prompt)