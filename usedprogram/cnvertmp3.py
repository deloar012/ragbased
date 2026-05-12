import os
import subprocess
import re

# FOLDER PATHS
VIDEO_DIR = "/home/deloar-hossen/Desktop/RAGPROJECT/videos"
AUDIO_DIR = "/home/deloar-hossen/Desktop/RAGPROJECT/audios"

# CREATE OUTPUT FOLDER
os.makedirs(AUDIO_DIR, exist_ok=True)

# SUPPORTED FORMATS
SUPPORTED_FORMATS = ('.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv')


#  CLEAN FILENAME FUNCTION
def clean_filename(file):
    name = os.path.splitext(file)[0]
    name = name.lower()
    name = name.replace(" ", "_")

    # Remove unwanted words
    bad_words = ["1080p","720p","480p","360p","240p","144p","hd","fullhd","4k","8k"]
    for word in bad_words:
        name = name.replace(word, "")

    # Keep only a-z, 0-9, _
    name = re.sub(r'[^a-z0-9_]', '', name)

    # Remove extra underscores
    name = re.sub(r'_+', '_', name)
    name = name.strip("_")

    # Fallback if empty
    if not name:
        name = "audio_file"

    return name[:80]


#  LOOP THROUGH FILES
for file in os.listdir(VIDEO_DIR):
    if file.lower().endswith(SUPPORTED_FORMATS):

        input_path = os.path.join(VIDEO_DIR, file)
        safe_name = clean_filename(file)

        # Create unique output filename
        output_path = os.path.join(AUDIO_DIR, f"{safe_name}.mp3")
        counter = 1
        while os.path.exists(output_path):
            output_path = os.path.join(AUDIO_DIR, f"{safe_name}_{counter}.mp3")
            counter += 1

        print(f"\n Processing: {file}")
        print(f" Output: {os.path.basename(output_path)}")

        # FFmpeg command
        command = [
            "ffmpeg",
            "-i", input_path,
            "-map", "0:a?",       # safe audio selection
            "-vn",
            "-c:a", "libmp3lame",
            "-b:a", "192k",
            "-y",
            output_path
        ]

        try:
            result = subprocess.run(command)

            # Check if file actually created
            if result.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                print(f" Success")
            else:
                print(f"Skipped (no audio or failed)")

        except Exception as e:
            print(f" Error: {e}")

print("\nAll conversions completed!")