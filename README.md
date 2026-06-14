# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
This system covers student reviews of professors at the University of Michigan, sourced from Rate My Professors. This knowledge is valuable because official course listings describe content but say nothing about teaching style, exam difficulty, workload, or how approachable a professor actually is. Students rely on word-of-mouth or scattered posts, my system makes that experience searchable in one place.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Rate My Professors | Text reviews | documents/gehring_bill_p1.txt |
| 2 | Rate My Professors | Text reviews | documents/gehring_bill_p2.txt |
| 3 | Rate My Professors | Text reviews | documents/guilmet_elizabeth_p1.txt  |
| 4 | Rate My Professors | Text reviews | documents/guilmet_elizabeth_p2.txt  |
| 5 | Rate My Professors | Text reviews | documents/jones_jennifer_p1.txt |
| 6 | Rate My Professors | Text reviews | documents/khan_pauline_p1.txt  |
| 7 | Rate My Professors | Text reviews | documents/khan_pauline_p2.txt  |
| 8 | Rate My Professors | Text reviews | documents/richards_janet_p1.txt  |
| 9 | Rate My Professors | Text reviews | documents/smith_stephen_p1.txt  |
| 10 | Rate My Professors | Text reviews | documents/smith_stephen_p2.txt  |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 300 characters

**Overlap:** 50 characters

**Why these choices fit your documents:** RateMyProfessor reviews are short, aboutu 1 to 5 sentences each. A 300-character chunk captures roughly one full review without merging multiple reviews together, which would make source attribution harder. The 50-character overlap makes sure that reviews near a chunk boundary don't get cut off mid-thought. Larger chunks would dilute the signal by blending multiple opinions; smaller ones would create fragments with no standalone meaning.


**Final chunk count:** 81 chunks across 10 documents

---
## Sample Chunks

**Chunk 1** (source: smith_stephen_p1.txt)
> "Dr. Smith is a great lecturer. He makes dense lectures easy to follow, and is very approachable. There weren't exams, so the class is overall less stressful than it likely..."

**Chunk 2** (source: smith_stephen_p2.txt)
> "are easy to follow and often includes interesting fun facts. He explains concepts very well and balances depth with understandability well. The class itself is pretty easy."

**Chunk 3** (source: gehring_bill_p1.txt)
> "n amazing professor who clearly cares about the course and students. Only thing I will say is that the demos in class do come in the exam so participate and don't brush them off. Exams do require a lo..."

**Chunk 4** (source: jones_jennifer_p1.txt)
> "According to student reviews, Dr. Jennifer Jones teaches WGS341, a class on Black queer studies. Students gave her a quality rating of 5.0 and a difficulty rating of 3.0."

**Chunk 5** (source: guilmet_elizabeth_p2.txt)
> "Teaching style is definitely intimidating. She has very high standards for students and is not afraid to call out bad work. However, that pushes us to work our best."
---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2 via sentence-transformers (local, no API key required)


**Production tradeoff reflection:** For a real deployment I'd look at larger models like OpenAI's `text-embedding-3-large` or `instructor-xl`. The main tradeoffs I'd weigh are context length (all-MiniLM caps at 256 tokens, which is fine for short reviews but wouldn't scale to longer documents), accuracy on domain-specific informal text (student slang and casual writing isn't what most embedding models were tuned on), latency at scale (local models add inference time when you have thousands of users), and cost (API-hosted models charge per token but remove infrastructure overhead). For a university app with mostly short-form text, a hosted model with better semantic accuracy would likely be worth it.


---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
> "You are a helpful assistant that answers questions about University of Michigan professors based solely on student reviews. Answer using only the information in the provided context. Always cite which source document(s) your answer came from. If the context does not contain enough information to answer the question, respond with: 'I don't have enough information on that based on the available student reviews.'"

**How source attribution is surfaced in the response:**
## Retrieval Test Results

**Query 1:** "What do students say about Stephen Smith's teaching style?"
Top chunks returned from: smith_stephen_p1.txt, smith_stephen_p2.txt
These chunks are relevant because they contain direct student descriptions of Dr. Smith's lecture style, approachability, and classroom behavior — exactly what the query asks for.

**Query 2:** "Which professors are known for being accessible outside of class?"
Top chunks returned from: jones_jennifer_p1.txt, smith_stephen_p1.txt, gehring_bill_p1.txt, richards_janet_p1.txt
These chunks are relevant because they contain language about professors caring about students, being approachable, and encouraging office hours — all signals of accessibility.

**Query 3:** "What do students say about Bill Gehring's exams?"
Top chunks returned from: gehring_bill_p1.txt, gehring_bill_p2.txt, smith_stephen_p2.txt
The Gehring chunks are relevant — they mention exam content and study requirements directly. The Smith chunk appearing in results is a weaker match and reflects the high distance scores (0.9+) discussed in the failure case below.

---

## Grounded Generation — Example Responses

**Example 1:**
Query: "What do students say about Stephen Smith's teaching style?"
Response: "According to student reviews, Dr. Stephen Smith is described as a great lecturer who makes dense lectures easy to follow and is very approachable (Source: smith_stephen_p1.txt, smith_stephen_p2.txt). He responds to emails quickly and gives lots of opportunity for feedback. One review also mentions that he plays the banjo sometimes in class."

**Example 2:**
Query: "Which professor is recommended for someone who wants a 5-star quality psychology course?"
Response: "Based on the available student reviews, Dr. Bill Gehring is recommended for a 5-star quality psychology course, specifically PSYCH240. Multiple reviews give him a 5.0 quality rating and praise his teaching style and care for students (Source: gehring_bill_p1.txt, gehring_bill_p2.txt)."

**Out-of-scope query:**
Query: "What is the weather in Paris?"
Response: "I don't have enough information on that based on the available student reviews."

---

## Query Interface

**Input field:** A text box labeled "Ask about a UMich professor" where the user types a natural language question.

**Output fields:** Two text boxes — "Answer" (the LLM-generated response grounded in retrieved chunks) and "Sources" (a list of the source filenames retrieved from ChromaDB).

**Sample interaction transcript:**

> **User:** What do students say about Bill Gehring's exams?
>
> **Answer:** According to student reviews, Bill Gehring's exams "do require a lot of studying but aren't impossible" (Source: gehring_bill_p1.txt). Students also mention that the in-class demos appear on exams, so participation matters.
>
> **Sources:**
> • gehring_bill_p1.txt
> • gehring_bill_p2.txt
---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 |What do students say about Stephen Smith's teaching style? |Engaging, easy to follow, approachable | Great lecturer, easy to follow, approachable, plays banjo in class |Relevant | Accurate |
| 2 | Which professors are known for being accessible outside of class? | Professors mentioning office hours or responsiveness | Dr. Jones, Dr. Smith, Dr. Gehring cited with supporting review text | Relevant | Accurate |
| 3 |What courses does Jennifer Jones teach and how do students rate them? | Jones's subject area, positive reviews | WGS341, Black queer studies, 5.0 quality rating, highly recommended | Relevant | Accurate |
| 4 |Which professor is recommended for a 5-star quality psychology course? | Professor with 5-star quality rating in psychology | Dr. Bill Gehring, PSYCH240, 5.0 quality rating | Relevant | Accurate |
| 5 | What do students say about Bill Gehring's exams? | Reviews mentioning exam style, difficulty, fairness | Exams require studying but aren't impossible; in-class demos appear on exams | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**"What do students say about Bill Gehring's teaching style?"


**What the system returned:** The system responded with "I don't have enough information on that based on the available student reviews" — even though Gehring reviews exist in the corpus — while also partially pulling a relevant chunk from gehring_bill_p2.txt. The sources panel returned mostly unrelated professor files.

**Root cause (tied to a specific pipeline stage):** The distance scores for all queries in this system are high (0.8–1.0), well above the ideal threshold of 0.5. This is a retrieval stage issue. RMP reviews are short, casual, and informal — the all-MiniLM-L6-v2 model wasn't fine-tuned on this kind of text, so semantic similarity scores are weak across the board. When the query is specific to one professor but the chunks are short fragments, the embedding can't reliably distinguish a Gehring chunk from a Smith chunk by topic alone.

**What you would change to fix it:** Store the professor's name as a metadata filter in ChromaDB and pre-filter by name before running semantic search. That way, a query about Gehring only searches Gehring chunks, and semantic ranking works on a much smaller, more relevant pool.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** The chunking strategy section of planning.md forced me to think about document structure before writing any code. Because I had already decided on 300-character chunks with 50-character overlap and written down the reasoning, when Claude Code generated `ingest.py` it matched my spec exactly. I didn't have to debug chunk size decisions mid-implementation.

**One way your implementation diverged from the spec, and why:** The spec assumed ChromaDB would run in-memory during ingestion and retrieval. In practice, `retrieve.py` couldn't access chunks stored by `ingest.py` because in-memory collections don't persist between processes. I switched to `PersistentClient(path="./chroma_db")` so the vector store survives across script runs. This wasn't in the original plan but was a necessary infrastructure fix to make the pipeline work end-to-end.
---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* My chunking strategy and retrieval approach sections from planning.md, plus a description of my document structure (short RMP review text files)
- *What it produced:* A complete `ingest.py` that loaded .txt files, cleaned whitespace, chunked at 300 characters with 50-character overlap, embedded with all-MiniLM-L6-v2, and stored in ChromaDB
- *What I changed or overrode:* The generated code used `chromadb.Client()` (in-memory), which meant chunks disappeared when the script exited. I directed Claude to switch to `PersistentClient(path="./chroma_db")` and add drop-and-recreate logic so re-running ingest doesn't create duplicate IDs

**Instance 2**

- *What I gave the AI:* My grounding requirement, output format spec (answer + sources), and the Gradio interface structure from the milestone instructions
- *What it produced:* `query.py` with the Groq client and system prompt, and `app.py` with a working Gradio Blocks interface including labeled input/output fields and Enter-key submission
- *What I changed or overrode:* I verified the system prompt matched my exact grounding instruction rather than a watered-down version, and confirmed source filenames were returned programmatically from ChromaDB metadata rather than relying on the LLM to cite them on its own
