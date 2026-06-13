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

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

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

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
