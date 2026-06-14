import os
import re
import chromadb
from sentence_transformers import SentenceTransformer

DOCUMENTS_DIR = "documents"
COLLECTION_NAME = "professor_reviews"
CHUNK_SIZE = 300
OVERLAP = 50


def clean_text(text):
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def main():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.Client()
    collection = client.create_collection(COLLECTION_NAME)

    all_ids = []
    all_embeddings = []
    all_documents = []
    all_metadatas = []

    txt_files = sorted(
        f for f in os.listdir(DOCUMENTS_DIR) if f.endswith(".txt")
    )

    for filename in txt_files:
        filepath = os.path.join(DOCUMENTS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            raw = f.read()

        text = clean_text(raw)
        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):
            doc_id = f"{filename}_chunk_{i}"
            all_ids.append(doc_id)
            all_documents.append(chunk)
            all_metadatas.append({"source": filename, "chunk_index": i})

    all_embeddings = model.encode(all_documents).tolist()

    collection.add(
        ids=all_ids,
        embeddings=all_embeddings,
        documents=all_documents,
        metadatas=all_metadatas,
    )

    print(f"Total chunks ingested: {len(all_ids)}")


if __name__ == "__main__":
    main()
