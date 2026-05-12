import whisper
import json
import torch
import os

device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", device)

model = whisper.load_model("small", device=device)

audios = os.listdir("audios/")
os.makedirs("chunks", exist_ok=True)

for audio in audios:
    if "_" in audio and audio.endswith(".mp3"):

        # remove .mp3
        name = os.path.splitext(audio)[0]
        parts = name.split("_")

        number = parts[1]
        title = " ".join(parts[2:])
        final_name = number + " " + title

        print(final_name)

        # correct path
        result = model.transcribe(f"audios/{audio}", task="translate")

        chunks = []
        for segment in result["segments"]:
            data = {
                "title": title,
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"]
            }
            chunks.append(data)

        with open(f"chunks/{final_name}.json", "w") as f:
            json.dump(chunks, f, indent=4)