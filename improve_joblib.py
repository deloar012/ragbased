import pandas as pd
import ollama
import numpy as np
import joblib

# -------------------------
# Load data
# -------------------------
df = joblib.load("embedding.joblib")

embedding_matrix = np.array(df["embedding"].tolist())

# Normalize embeddings (important for cosine via dot product)
embedding_matrix = embedding_matrix / np.linalg.norm(
    embedding_matrix, axis=1, keepdims=True
)

# -------------------------
# User Query
# -------------------------
query = input("Ask >> ")

# -------------------------
# Get query embedding
# -------------------------
response = ollama.embed(
    model="bge-m3",
    input=query
)

query_embedding = np.array(response["embeddings"][0])

# Normalize query embedding
query_embedding = query_embedding / np.linalg.norm(query_embedding)

# -------------------------
# FAST similarity (dot product)
# -------------------------
similarities = np.dot(embedding_matrix, query_embedding)

# Copy dataframe (avoid overwriting original)
df_copy = df.copy()
df_copy["similarity"] = similarities

# -------------------------
# Top K results
# -------------------------
top_results = df_copy.sort_values(
    "similarity",
    ascending=False
).head(5)

# -------------------------
# Build context
# -------------------------
context = "\n\n".join(
    f"{row['text']}"
    for _, row in top_results.iterrows()
)

# -------------------------
# Prompt (important part)
# -------------------------
prompt = f"""
You are a helpful AI assistant.

Use ONLY the context below to answer the question.
If the answer is not in the context, say:
"I could not find the answer in the provided context."

Give a clear, complete, ChatGPT-style answer.

Context:
{context}

Question:
{query}

Answer:
"""

# -------------------------
# Generate response
# -------------------------
chat_response = ollama.chat(
    model="qwen3:8b",
    options={
        "temperature": 0.2
    },
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

# -------------------------
# FINAL OUTPUT (ONLY ANSWER)
# -------------------------
print("\n===== ANSWER =====\n")
print(chat_response["message"]["content"])