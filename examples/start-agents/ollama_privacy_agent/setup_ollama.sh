#!/bin/bash
echo "Installing Ollama binary..."
curl -fsSL https://ollama.com/install.sh | sh
echo "Starting Ollama server..."
ollama serve > ./data/ollama_server.log 2>&1 &
echo "Waiting 10s for server..."
sleep 10 
echo "Pulling Llama 3.1..."
ollama pull llama3.1.1
echo "Setup Complete."
