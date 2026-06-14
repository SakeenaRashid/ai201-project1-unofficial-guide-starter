import chromadb
from sentence_transformers import SentenceTransformer

COLLECTION_NAME = "professor_reviews"

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(COLLECTION_NAME)


def retrieve(query, k=5):
    embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
    chunks = []
    for text, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append({
            "text": text,
            "source": meta["source"],
            "distance": dist,
        })
    return chunks


if __name__ == "__main__":
    queries = [
        "What do students say about the professor's teaching style?",
        "Which professors are good at explaining difficult concepts?",
        "What do students say about exams and grading?",
    ]

    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 60)
        for i, chunk in enumerate(retrieve(query), 1):
            print(f"[{i}] Source: {chunk['source']}  Distance: {chunk['distance']:.4f}")
            print(f"    {chunk['text'][:200].strip()}")
            print()
