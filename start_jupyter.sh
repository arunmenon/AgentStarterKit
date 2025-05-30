#!/bin/bash
echo "🎨 Starting AgentFlow Studio..."

# Activate virtual environment
source agent_env/bin/activate

# Start Ollama if not running
if ! pgrep -f "ollama serve" > /dev/null; then
    echo "Starting Ollama service..."
    nohup ollama serve > ollama.log 2>&1 &
    sleep 3
fi

# Launch Jupyter
echo "Launching AgentFlow Studio..."
jupyter lab --NotebookApp.token='' --NotebookApp.password=''
