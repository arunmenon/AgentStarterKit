#!/bin/bash

echo "🤖 Setting up Agent Starter Kit environment..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv agent_env

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source agent_env/bin/activate

# Create requirements.txt
echo "📋 Creating requirements.txt..."
cat > requirements.txt << EOF
# Core AI and Agent Libraries
openai>=1.3.0

# Data Processing
pandas>=1.5.0
numpy>=1.24.0
matplotlib>=3.6.0
seaborn>=0.12.0

# Networking and APIs
requests>=2.28.0
aiohttp>=3.8.0

# Graph and Planning
networkx>=3.0
python-dotenv>=1.0.0

# Jupyter and Development
jupyter>=1.0.0
jupyterlab>=3.5.0
ipywidgets>=8.0.0

# Utilities
schedule>=1.2.0
pyyaml>=6.0
EOF

# Install dependencies
echo "⬇️ Installing Python packages..."
pip install -r requirements.txt

# Create .env template
echo "🔑 Creating .env template..."
cat > .env << EOF
# Add your API keys here
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Other services
GMAIL_APP_PASSWORD=your_gmail_app_password
DATABASE_URL=sqlite:///agent_data.db
EOF

# Create workspace directory
echo "📁 Creating workspace directories..."
mkdir -p agent_workspace
mkdir -p shared_utils

# Create shared utils init file
touch shared_utils/__init__.py

# Create README
echo "📖 Creating README..."
cat > README.md << EOF
# Agent Starter Kit

A comprehensive curriculum for building autonomous AI agents.

## Setup

1. Run the setup script: \`bash setup.sh\`
2. Add your API keys to the \`.env\` file
3. Launch Jupyter: \`jupyter lab\`

## Modules

- **Chapter 1**: Agent Foundations - Basic autonomous agents with ReAct pattern
- **Chapter 2**: Memory and Learning - Sophisticated memory systems and learning
- **Chapter 3**: Tool Integration - Real-world tool integration and workflows  
- **Chapter 4**: Planning and Goals - Hierarchical planning and goal decomposition

## Usage

Start with Chapter 1 and work through the modules sequentially. Each notebook builds on the previous ones.
EOF

echo "✅ Setup complete!"
echo "📝 Next steps:"
echo "   1. Add your OpenAI API key to .env file"
echo "   2. Run: source agent_env/bin/activate"
echo "   3. Run: jupyter lab"
echo "   4. Open chapter_1/01_agent_foundations.ipynb to start"