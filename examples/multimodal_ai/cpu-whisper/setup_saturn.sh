#!/bin/bash

# Exit on any error
set -e

echo "--- 1. Environment Pre-flight Check ---"

# Update package list
echo "Updating system package repositories..."
sudo apt update -y

# Install FFmpeg and Python dependencies
echo "Installing FFmpeg and Python tools..."
sudo apt install -y ffmpeg python3-pip python3-venv

# Verify FFmpeg installation
if ffmpeg -version > /dev/null 2>&1; then
    echo "SUCCESS: FFmpeg is installed and ready."
else
    echo "ERROR: FFmpeg installation failed."
    exit 1
fi

echo "--- 2. Setting Up Python Environment ---"

# Create and activate a virtual environment
echo "Creating virtual environment: whisper_env..."
python3 -m venv whisper_env
source whisper_env/bin/activate

# Install OpenAI Whisper
echo "Installing OpenAI Whisper..."
pip install -U openai-whisper


# Install core transcription and visualization dependencies
pip install openai-whisper librosa matplotlib

# Verify Whisper installation
if whisper --help > /dev/null 2>&1; then
    echo "SUCCESS: Whisper AI is installed."
else
    echo "ERROR: Whisper AI installation failed."
    exit 1
fi

echo "--- Setup Complete ---"
echo "You can now run your transcription tests using 'whisper <audio_file>'."