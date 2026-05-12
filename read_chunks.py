import os
import json
import ollama

folder = "json/"   # your folder name

# -----------------------------
# 1. Embedding function
# -----------------------------
def create_embeddings(text):
    response = ollama.embed(
        model="bge-m3",
        input=text
    )
    return response["embeddings"][0]


# -----------------------------
# 2. Loop through all JSON files
# -----------------------------
for file in os.listdir(folder):

    if not file.endswith(".json"):
        continue

    file_path = os.path.join(folder, file)
    print(f"📂 Processing: {file}")

    # -----------------------------
    # 3. Load JSON
    # -----------------------------
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error reading {file}: {e}")
        continue

    # -----------------------------
    # 4. Process chunks
    # -----------------------------
    chunks = data.get("chunks", [])

    if not chunks:
        print("⚠️ No chunks found")
        continue

    for chunk in chunks:
        text = chunk.get("text", "").strip()

        # skip bad text
        if not text:
            print("⚠️ Skipped bad text")
            continue

        # skip if already embedded (important!)
        if "embedding" in chunk:
            continue

        try:
            chunk["embedding"] = create_embeddings(text)
        except Exception as e:
            print(f"❌ Embedding error: {e}")
            continue

    # -----------------------------
    # 5. Save updated JSON
    # -----------------------------
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"✅ Done: {file}")
    except Exception as e:
        print(f"❌ Save error: {e}")