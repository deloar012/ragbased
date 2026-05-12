import whisper
import json
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", device)

model = whisper.load_model("small").to(device)
result= model.transcribe("audios/test_10s.mp3",
                         task="translate")
result["segments"]=result["segments"]
chunks=[]
for segment in result["segments"]:
    data={
        "start":segment["start"],
        "end": segment["end"],
        "text":segment["text"]
    }
    chunks.append(data)
print(chunks)
