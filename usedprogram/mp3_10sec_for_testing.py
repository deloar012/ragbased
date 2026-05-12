import subprocess

input_file = "/home/deloar-hossen/Desktop/RAGPROJECT/audios/lecture_2_strings_conditional_statements_python_full_course.mp3"
output_file = "/home/deloar-hossen/Desktop/RAGPROJECT/audios/test_10s.mp3"

command = [
    "ffmpeg",
    "-ss", "0",        # start time (0 sec)
    "-t", "10",        # duration (10 sec)
    "-i", input_file,
    "-c", "copy",      # no re-encoding (fast)
    "-y",              # overwrite if exists
    output_file
]

result = subprocess.run(command)

if result.returncode == 0:
    print("✅ 10-second audio created:", output_file)
else:
    print("❌ Failed to create sample")