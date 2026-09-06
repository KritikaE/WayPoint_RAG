from retrieve import search, rerank_results, process_query

query = input("Enter a retrieval test query: ")

query = process_query(query)

results = search(query, n_results=5)
results = rerank_results(query, results)

print("\n" + "=" * 80)
print("RETRIEVAL RESULTS")
print("=" * 80)

for i, metadata in enumerate(results["metadatas"][0]):
    distance = results["distances"][0][i]

    print(f"\nRESULT {i + 1}")
    print("-" * 40)
    print(f"Condition : {metadata.get('condition', 'N/A')}")
    print(f"Title     : {metadata.get('title', 'N/A')}")
    print(f"Pages     : {metadata.get('printed_pages', 'N/A')}")
    print(f"Distance  : {distance:.4f}")