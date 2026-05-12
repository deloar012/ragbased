import pandas as pd
import ollama
import numpy as np
import joblib
from sklearn.metrics.pairwise import cosine_similarity

# Load dataframe
df = joblib.load("embedding.joblib")

# Convert embeddings column to numpy array once
embedding_matrix = np.array(df["embedding"].tolist())

# User query
query = input("Tell me what you want to ask >> ")

# Generate query embedding
response = ollama.embeddings(
    model="bge-m3",
    prompt=query
)

query_embedding = np.array(response["embedding"]).reshape(1, -1)

# FAST cosine similarity
similarities=cosine_similarity(
    query_embedding,
    embedding_matrix
)[0]

# Add similarity scores
df["similarity"] = similarities
print(df.columns)
# Top results
top_results = df.nlargest(10, "similarity")

# Print top results with details
print("\n===== TOP RESULTS =====\n")
for idx, (_, row) in enumerate(top_results.iterrows(), 1):
    print(f"{idx}. Course: {row['title']}")
    print(f"   Time: {row['start']:.1f}s - {row['end']:.1f}s")
    print(f"   Text: {row['text']}")
    print(f"   Similarity Score: {row['similarity']:.4f}\n")

# Build context
context = "\n\n".join(top_results["text"].tolist())

# Prompt
prompt = f"""
Answer the question using ONLY the context below.

Context:
{context}

Question:
{query}

Answer:
"""

# Generate response
chat_response = ollama.chat(
    model="qwen3:8b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print("\n===== ANSWER =====\n")
print(chat_response["message"]["content"])