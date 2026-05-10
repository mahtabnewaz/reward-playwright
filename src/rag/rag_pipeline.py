import os
import json
import sys
import chromadb
from chromadb.utils import embedding_functions

CORPUS_FILE = "data/playwright_corpus/corpus.json"
CHROMA_DIR = "data/chroma_db"
COLLECTION_NAME = "playwright_tests"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
    collection = client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=embedding_fn)
    return collection


def build_index():
    """Embed corpus into ChromaDB. Run once to set up."""
    print(f"Loading corpus from {CORPUS_FILE}...")
    with open(CORPUS_FILE) as f:
        corpus = json.load(f)
    print(f"Found {len(corpus)} examples.")

    collection = get_collection()

    # Clear existing data to avoid duplicates
    try:
        existing = collection.get()
        if existing["ids"]:
            collection.delete(ids=existing["ids"])
            print(f"Cleared {len(existing['ids'])} existing entries.")
    except Exception:
        pass

    ids = [item["id"] for item in corpus]
    documents = [item["description"] for item in corpus]
    metadatas = [{"category": item["category"], "code": item["code"]} for item in corpus]

    print("Embedding and indexing...")
    collection.add(ids=ids, documents=documents, metadatas=metadatas)
    print(f"Indexed {collection.count()} examples successfully.")


def retrieve(query, k=5):
    """Retrieve top-k similar Playwright tests for a given requirement."""
    collection = get_collection()
    results = collection.query(query_texts=[query], n_results=k)
    examples = []
    for i in range(len(results["ids"][0])):
        examples.append({
            "id": results["ids"][0][i],
            "description": results["documents"][0][i],
            "category": results["metadatas"][0][i]["category"],
            "code": results["metadatas"][0][i]["code"],
            "distance": round(results["distances"][0][i], 3),
        })
    return examples


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        build_index()
    elif len(sys.argv) > 1 and sys.argv[1] == "test":
        query = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "verify login button is visible"
        print(f"\nQuery: {query}\n")
        results = retrieve(query, k=3)
        for r in results:
            print(f"[{r['id']}] ({r['category']}) distance={r['distance']}")
            print(f"  Description: {r['description']}")
            print(f"  Code preview: {r['code'][:80]}...\n")
    else:
        print("Usage:")
        print("  python src/rag/rag_pipeline.py build       - Build the index")
        print("  python src/rag/rag_pipeline.py test <query> - Test retrieval")
