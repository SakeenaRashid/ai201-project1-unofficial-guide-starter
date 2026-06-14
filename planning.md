# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
My domain is student reviews of professors at the University of Michigan, sourced from RateMyProfessors.com 
This knowledge is valuable because official course listings describe course content but reveal
nothing about teaching style, exam difficulty, accessibility, or workload. Students rely on
word-of-mouth or scattered forum posts this system makes that knowledge searchable in one place.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | RateMyProfessors.com |student reviews on professors | https://www.ratemyprofessors.com/professor/1080164 |
| 2 | RateMyProfessors.com |student reviews on professors | https://www.ratemyprofessors.com/professor/1080164 |
| 3 | RateMyProfessors.com |student reviews on professors | https://www.ratemyprofessors.com/professor/1787414 |
| 4 | RateMyProfessors.com |student reviews on professors | https://www.ratemyprofessors.com/professor/1787414 |
| 5 | RateMyProfessors.com |student reviews on professors | https://www.ratemyprofessors.com/professor/2542205 |
| 6 | RateMyProfessors.com |student reviews on professors | https://www.ratemyprofessors.com/professor/2585042 | 
| 7 | RateMyProfessors.com |student reviews on professors | https://www.ratemyprofessors.com/professor/2585042 |
| 8 | RateMyProfessors.com |student reviews on professors | https://www.ratemyprofessors.com/professor/287242 |
| 9 | RateMyProfessors.com |student reviews on professors | https://www.ratemyprofessors.com/professor/287242 |
| 10 | RateMyProfessors.com |student reviews on professors| https://www.ratemyprofessors.com/professor/38555 |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 300 characters

**Overlap:** 50 characters

**Reasoning:** RateMyProfessor reviews are short (about 1–5 sentences each). A 300 character chunk captures roughly one full review without splitting it awkwardly. Overlap of 50 characters ensures that reviews near a chunk boundary aren't lost. Larger chunks would merge multiple reviews together, making attribution harder.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers (local, no API key required

**Top-k:** 5

**Production tradeoff reflection:** For a production deployment I would evaluate larger models like `text-embedding-3-large` (OpenAI) or `instructor-xl` for higher accuracy on domain-specific text. Key tradeoffs: context length (all-MiniLM caps at 256 tokens, which is fine for short reviews but not long guides), latency (local models add inference time at scale), and multilingual support (relevant if the user base includes non-English speakers). For a university app, latency and cost would likely favor a hosted API model over a local one.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say about Stephen Smith's teaching style? | Engaging, uses real-world examples, good at explaining complex topics |
| 2 |  Which professors are known for being accessible outside of class?  | Should return professors with reviews mentioning office hours or responsiveness  |
| 3 |  What courses does Jennifer Jones teach and how do students rate them?  |  [Jone's subject] related courses, positive reviews about depth and rigor |
| 4 |  Which professor is recommended for someone who wants a 5-star quality psychology course? |  Should return prof with reviews mentioning difficulty and learning outcome and/or 5 rating for quality |
| 5 | What do students say about Bill Gehring's exams? |  Reviews mentioning exam style, difficulty, or fairness |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. **Short review text and chunk boundary splits:** Because reviews are only a few sentences, a chunk boundary could split a review mid-thought, causing the retrieval model to return incomplete context. This is mitigated by keeping chunk size small (300 chars) with overlap.

2. **Lack of negative signal:** Only positive reviews are included, so the system may over-recommend every professor equally for queries like "easiest professor" — the corpus doesn't contain the contrast needed to differentiate on that axis. This is an expected limitation and could be a good failure case for the evaluation report.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->
Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation

(.txt files)     (300 char,    (all-MiniLM-L6-v2,       (ChromaDB    (Groq /

documents/         50 overlap,    sentence-transformers)    top-k=5)    llama-3.3-70b)

plain text)

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
I will give Claude the Chunking Strategy section of this file and ask it to implement `ingest.py` — a script that reads all `.txt` files from `documents/`, splits them into 300-character chunks with 50-character overlap, and stores them in ChromaDB with source metadata. I will verify the output by checking chunk count and spot-checking 3 chunks manually.

**Milestone 4 — Embedding and retrieval:**
I will give Claude the Retrieval Approach section and ask it to implement `retrieve.py` a function that takes a query string, embeds it with all-MiniLM-L6-v2, queries ChromaDB for top-5 results, and returns chunks with source attribution. I will test it with all 5 evaluation questions and check that returned chunks are relevant.
**Milestone 5 — Generation and interface:**
I will give Claude the full pipeline spec and ask it to implement `app.py` using Gradio, a query interface that takes a user question, retrieves the top-5 chunks, passes them to Groq (llama-3.3-70b-versatile) with a grounding prompt, and displays the response with source citations. I will verify grounding by asking an out-of-scope question and confirming refusal.