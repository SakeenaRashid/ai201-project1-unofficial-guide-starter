import os
from dotenv import load_dotenv
from groq import Groq
from retrieve import retrieve

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = (
    "You are a helpful assistant that answers questions about University of Michigan professors "
    "based solely on student reviews. Answer using only the information in the provided context. "
    "Always cite which source document(s) your answer came from. If the context does not contain "
    "enough information to answer the question, respond with: "
    "'I don't have enough information on that based on the available student reviews.'"
)


def ask(question):
    chunks = retrieve(question, k=5)

    context = "\n\n".join(
        f"[Source: {chunk['source']}]\n{chunk['text']}" for chunk in chunks
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
    )

    answer = response.choices[0].message.content
    sources = list({chunk["source"] for chunk in chunks})

    return {"answer": answer, "sources": sources}
