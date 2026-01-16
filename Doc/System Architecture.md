# System Architecture

The system is a Retrieval-Augmented Generation (RAG) agent for the medical domain. It integrates external knowledge, an LLM, and safety checks.

Components:

1. Document Storage

medical_docs.txt contains structured medical knowledge (drugs, side effects, health conditions).

Documents are split into chunks for embeddings.

2. Embeddings & Vector Store

GoogleGenerativeAIEmbeddings with default model "models/embedding-001" generates semantic embeddings.

Chroma vector store stores embeddings and allows retrieval of relevant chunks.

Retrieval is controlled via top-k search.

3. Retriever

Wraps vectordb and returns the most relevant chunks for a given query.

4. LLM Layer

ChatGoogleGenerativeAI (Gemini-2.0-flash-exp) generates responses based on retrieved context.

Temperature: 0.1 for more deterministic answers.

5. Maker–Checker Agents

Maker: Generates initial answer using LLM + context.

Checker: Reviews output for correctness, safety, and completeness.

Refines answer if any issue is detected.

5. Safety Layer

Input validation for unsafe or malformed queries.

Blocked keywords: ["prescribe", "diagnose", "kill", "suicide", "bomb"].

Safe generation: LLM uses retrieved context only, and outputs are sanitized before returning.
