import torch
import whisper
import os
import urllib.request

# 1. Hardware Detection
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Testing on Device: {device.upper()}")

# 2. Verified Stable Test Audio
# This is a sample1.flac file from Hugging Face spaces
audio_url = "https://huggingface.co/spaces/speechbox/whisper-restore-punctuation/resolve/main/sample1.flac"
audio_file = "sample1.flac"

try:
    if not os.path.exists(audio_file):
        print(f"Downloading sample audio from {audio_url}...")
        # Standard headers to ensure the server accepts the request
        req = urllib.request.Request(audio_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(audio_file, 'wb') as out_file:
            out_file.write(response.read())
        print("Download complete.")
except Exception as e:
    print(f"Error downloading audio: {e}")
    exit(1)

# 3. Load Model and Transcribe
print("Loading Whisper 'base' model...")
# The 'base' model requires ~1GB VRAM and is ~7x faster than the large model
model = whisper.load_model("base", device=device)

print("Starting transcription...")
# Ensure ffmpeg is installed as it is required for audio processing
result = model.transcribe(audio_file)

# 4. Final Output Verification
print("-" * 30)
print("TRANSCRIPT OUTPUT:")
print(result["text"].strip())
print("-" * 30)