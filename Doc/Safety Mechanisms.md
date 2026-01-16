2️⃣ Safety Mechanisms

1. Input Validation

Queries are checked for unsafe keywords and empty strings.

Unsafe queries are blocked immediately.

2. Safe LLM Usage

LLM is provided only relevant context from the vector store.

Temperature is low (0.1) for deterministic and controlled outputs.

3. Maker–Checker Loop

Ensures answers are reviewed before delivery.

Refinement step prevents hallucinations and ensures consistency with documents.

4. Output Sanitization

Ensures answers do not include unsafe or forbidden instructions (like prescribing drugs).
