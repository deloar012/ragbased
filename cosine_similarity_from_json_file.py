import os
import json
import ollama
import pandas as pd
import numpy as np
import joblib
from sklearn.metrics.pairwise import cosine_similarity
# load data from json file
folder="json/"
all_chunks=[]
for file in os.listdir(folder):
    if file.endswith(".json"):
        full_path=os.path.join(folder,file)
        with open(full_path,"r",encoding="utf-8") as f:
            data=json.load(f)
            if "chunks" in data:
                all_chunks.extend(data["chunks"])
# print("total chunks:",len(all_chunks))

# show first chunk
# print(all_chunks)

df=pd.DataFrame(all_chunks)
df=df[df["embedding"].notna()]
#save this dataframe
# joblib.dump(df,"embedding.joblib")
# Generate embedding for the user query
query=input("Told me whats you ask >> ")
response=ollama.embeddings(
    model="bge-m3",
    prompt=query
)
query_embedding=response["embedding"]
print("Embedding lenth;",len(query_embedding))
print(query_embedding)

# cosine similarity using for compare embedding with all chunks embeddings 
df["similarity"]=df["embedding"].apply(
    lambda x:cosine_similarity(
        [query_embedding],
        [x]

    )[0][0]
)
# sort by highest similarity
top_result=df.sort_values(
    by="similarity",
    ascending=False
)
# show top 5 matches
print(top_result[["text","similarity"]].head(5))