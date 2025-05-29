#!/bin/bash
echo "🛑 Stopping AgentFlow Studio Services..."

# Stop Jupyter
echo "Stopping Jupyter..."
jupyter notebook stop 8888 2>/dev/null || true
pkill -f jupyter-lab 2>/dev/null || true

# Stop Ollama
echo "Stopping Ollama..."
pkill -f "ollama serve" 2>/dev/null || true

echo "✅ All services stopped"
