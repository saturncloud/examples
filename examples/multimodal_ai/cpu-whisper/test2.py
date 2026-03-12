import whisper
import torch
import librosa
import matplotlib.pyplot as plt

# Check hardware
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Running on: {device.upper()}")

# Load model and transcribe
model = whisper.load_model("base", device=device)
result = model.transcribe("sample1.flac")

# Export Transcript
with open("transcript.txt", "w") as f:
    f.write(result["text"])

# Generate Waveform
y, sr = librosa.load("sample1.flac")
plt.figure(figsize=(10, 4))
librosa.display.waveshow(y, sr=sr)
plt.savefig("waveform.png")

print("Verification Complete: Check transcript.txt and waveform.png")