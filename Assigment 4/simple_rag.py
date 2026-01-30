# Lab 2A: Simple RAG using TF-IDF and Cosine Similarity
import os
import math
from collections import Counter

# ---------- Helper Functions ----------

def tokenize(text):
    """Basic text tokenizer: lowercases and splits by whitespace"""
    return text.lower().split()

def compute_tf(document_tokens):
    """Compute term frequency for a document"""
    tf = Counter(document_tokens)
    total_terms = len(document_tokens)
    return {term: count / total_terms for term, count in tf.items()}

def compute_idf(documents_tokens):
    """Compute inverse document frequency for all terms"""
    import math
    N = len(documents_tokens)
    idf = {}
    all_terms = set(term for doc in documents_tokens for term in doc)
    for term in all_terms:
        containing_docs = sum(1 for doc in documents_tokens if term in doc)
        idf[term] = math.log((N + 1) / (containing_docs + 1)) + 1  # smoothing
    return idf

def compute_tfidf(tf, idf):
    """Compute TF-IDF vector"""
    return {term: tf.get(term, 0) * idf.get(term, 0) for term in idf.keys()}

def cosine_similarity(vec1, vec2):
    """Compute cosine similarity between two vectors"""
    dot_product = sum(vec1[k] * vec2[k] for k in vec1.keys())
    magnitude1 = math.sqrt(sum(v**2 for v in vec1.values()))
    magnitude2 = math.sqrt(sum(v**2 for v in vec2.values()))
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    return dot_product / (magnitude1 * magnitude2)

# ---------- Step 1: Upload documents ----------
num_docs = int(input("How many documents do you want to upload? "))

documents = []
doc_names = []

for i in range(num_docs):
    path = input(f"Enter path for document {i+1}: ")
    if not os.path.isfile(path):
        print("Invalid file path. Skipping this document.")
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        documents.append(content)
        doc_names.append(os.path.basename(path))

# ---------- Step 2: Tokenize and vectorize ----------
documents_tokens = [tokenize(doc) for doc in documents]

# Compute IDF for all terms
idf = compute_idf(documents_tokens)

# Compute TF-IDF vectors for documents
document_vectors = []
for doc_tokens in documents_tokens:
    tf = compute_tf(doc_tokens)
    tfidf = compute_tfidf(tf, idf)
    document_vectors.append(tfidf)

# ---------- Step 3: Ask user for query ----------
query = input("Enter your query: ")
query_tokens = tokenize(query)
query_tf = compute_tf(query_tokens)
query_vector = compute_tfidf(query_tf, idf)

# ---------- Step 4: Compute cosine similarity ----------
similarities = [cosine_similarity(query_vector, doc_vec) for doc_vec in document_vectors]

# ---------- Step 5: Find most relevant document ----------
if similarities:
    max_index = similarities.index(max(similarities))
    print(f"\nMost relevant document: {doc_names[max_index]}")
    print(f"Cosine similarity: {similarities[max_index]:.4f}")
    print("\nDocument content preview:")
    print(documents[max_index][:500], "...")  # show first 500 chars
else:
    print("No valid documents were uploaded.")
