#!/bin/bash

# AgentStarterKit - Zero-Friction End-to-End Installer
# ====================================================
# One command to rule them all: ./install.sh
# 
# This script provides a complete, automated setup experience:
# • Virtual environment with all dependencies
# • Ollama installation and Qwen2.5 model
# • Jupyter environment ready to launch
# • Automatic notebook opening in browser
#
# Zero cognitive load - just run and start building agents!

set -e  # Exit on any error

# Colors for beautiful output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# ASCII Art Banner
show_banner() {
    echo -e "${CYAN}"
    cat << 'EOF'
    ___                   __  _____ __            __            __ __ _ __ 
   /   | ____ ____  ____  / /_/ ___// /_____ ______/ /____  _____/ //_/(_) /_
  / /| |/ __ `/ _ \/ __ \/ __/\__ \/ __/ __ `/ ___/ __/ _ \/ ___/ ,<  / / __/
 / ___ / /_/ /  __/ / / / /_ ___/ / /_/ /_/ / /  / /_/  __/ /  / /| |/ / /_  
/_/  |_\__, /\___/_/ /_/\__//____/\__/\__,_/_/   \__/\___/_/  /_/ |_/_/\__/  
      /____/                                                                  

EOF
    echo -e "${NC}"
    echo -e "${BOLD}🚀 Zero-Friction Agent Development Environment${NC}"
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# Progress tracking
TOTAL_STEPS=8
CURRENT_STEP=0

# Helper functions
show_step() {
    CURRENT_STEP=$((CURRENT_STEP + 1))
    echo -e "\n${BLUE}[$CURRENT_STEP/$TOTAL_STEPS]${NC} ${BOLD}$1${NC}"
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_status() {
    echo -e "${BLUE}  ▶${NC} $1"
}

print_success() {
    echo -e "${GREEN}  ✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}  ⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}  ❌${NC} $1"
}

print_info() {
    echo -e "${PURPLE}  ℹ️${NC} $1"
}

# Spinner for long operations
spin() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

# Error handler with helpful recovery suggestions
error_handler() {
    local line_no=$1
    local error_code=$2
    echo ""
    print_error "Installation failed at line $line_no with error code $error_code"
    echo ""
    print_info "💡 Quick fixes to try:"
    print_info "  1. Check your internet connection"
    print_info "  2. Ensure you have 10GB+ free disk space"
    print_info "  3. Close memory-intensive applications"
    print_info "  4. Try running with: bash -x install.sh (for debug output)"
    echo ""
    print_info "📚 For help, check our troubleshooting guide or open an issue"
    exit $error_code
}

trap 'error_handler ${LINENO} $?' ERR

# Check Python installation and version
check_python() {
    show_step "Checking Python Installation"
    
    # Try to find Python 3
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        # Check if 'python' is Python 3
        if python --version 2>&1 | grep -q "Python 3"; then
            PYTHON_CMD="python"
        else
            print_error "Python 3 is required but not found"
            print_info "Install Python 3.8+ from https://python.org"
            exit 1
        fi
    else
        print_error "Python not found in PATH"
        print_info "Install Python 3.8+ from https://python.org"
        exit 1
    fi
    
    # Check Python version
    PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    print_info "Found Python: $PYTHON_CMD (version $PYTHON_VERSION)"
    
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
        print_error "Python 3.8+ required, found $PYTHON_VERSION"
        exit 1
    fi
    
    print_success "Python $PYTHON_VERSION ✓"
}

# System requirements check
check_system_requirements() {
    show_step "Checking System Requirements"
    
    # Check OS
    print_status "Checking operating system..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        OS_TYPE="macOS"
        print_success "macOS detected ✓"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS_TYPE="Linux"
        print_success "Linux detected ✓"
    else
        print_error "Unsupported OS: $OSTYPE"
        print_info "This installer supports macOS and Linux only"
        exit 1
    fi
    
    # Check memory
    print_status "Checking system memory..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        TOTAL_MEM_GB=$(( $(sysctl -n hw.memsize) / 1024 / 1024 / 1024 ))
    else
        TOTAL_MEM_GB=$(free -g | awk '/^Mem:/{print $2}')
    fi
    
    if [ "$TOTAL_MEM_GB" -lt 8 ]; then
        print_warning "Limited memory: ${TOTAL_MEM_GB}GB (8GB+ recommended)"
        print_info "The system will work but may be slower"
    else
        print_success "Memory: ${TOTAL_MEM_GB}GB ✓"
    fi
    
    # Check disk space
    print_status "Checking disk space..."
    AVAILABLE_SPACE_GB=$(df . | awk 'NR==2 {print int($4/1024/1024)}')
    
    if [ "$AVAILABLE_SPACE_GB" -lt 10 ]; then
        print_error "Insufficient disk space: ${AVAILABLE_SPACE_GB}GB (10GB+ required)"
        exit 1
    else
        print_success "Disk space: ${AVAILABLE_SPACE_GB}GB available ✓"
    fi
    
    # Check internet
    print_status "Checking internet connection..."
    if ! curl -s --connect-timeout 5 https://ollama.ai > /dev/null; then
        print_error "No internet connection detected"
        print_info "Internet is required to download models and packages"
        exit 1
    else
        print_success "Internet connection ✓"
    fi
}

# Create and activate virtual environment
setup_virtual_environment() {
    show_step "Setting Up Python Virtual Environment"
    
    # Remove old environment if exists
    if [ -d "agent_env" ]; then
        print_warning "Existing virtual environment found"
        read -p "  Remove and recreate? (recommended) [Y/n]: " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
            print_status "Removing old environment..."
            rm -rf agent_env
        fi
    fi
    
    # Create new virtual environment
    print_status "Creating virtual environment 'agent_env'..."
    $PYTHON_CMD -m venv agent_env &
    spin $!
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source agent_env/bin/activate
    
    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip --quiet
    
    print_success "Virtual environment ready ✓"
}

# Install Python dependencies
install_python_dependencies() {
    show_step "Installing Python Dependencies"
    
    # Create comprehensive requirements.txt
    print_status "Creating requirements.txt..."
    cat > requirements.txt << 'EOF'
# Core AI and Agent Libraries
openai>=1.3.0
anthropic>=0.7.0

# Data Processing & Analysis
pandas>=1.5.0
numpy>=1.24.0
matplotlib>=3.6.0
seaborn>=0.12.0
plotly>=5.13.0

# Machine Learning & NLP
scikit-learn>=1.2.0
transformers>=4.25.0
tokenizers>=0.13.0

# Networking and APIs
requests>=2.28.0
aiohttp>=3.8.0
httpx>=0.23.0
websocket-client>=1.4.0

# Database & Storage
sqlalchemy>=2.0.0
redis>=4.4.0
pymongo>=4.3.0

# Agent Development
langchain>=0.0.200
guidance>=0.0.64
semantic-kernel>=0.3.0

# Graph and Planning
networkx>=3.0

# Environment Management
python-dotenv>=1.0.0
pyyaml>=6.0

# Jupyter and Development
jupyter>=1.0.0
jupyterlab>=3.5.0
notebook>=6.5.0
ipywidgets>=8.0.0
ipykernel>=6.20.0
nbformat>=5.7.0

# Code Quality
black>=22.12.0
flake8>=6.0.0
mypy>=0.991
pre-commit>=2.21.0

# Testing
pytest>=7.2.0
pytest-asyncio>=0.20.0
pytest-cov>=4.0.0

# Utilities
tqdm>=4.64.0
rich>=13.0.0
click>=8.1.0
schedule>=1.2.0
tenacity>=8.1.0

# Documentation
sphinx>=5.3.0
mkdocs>=1.4.0
mkdocs-material>=8.5.0
EOF

    # Install dependencies with progress
    print_status "Installing packages (this may take 2-5 minutes)..."
    pip install -r requirements.txt --quiet --progress-bar on
    
    print_success "All Python packages installed ✓"
}

# Install and configure Ollama
install_ollama() {
    show_step "Installing Ollama"
    
    # Check if already installed
    if command -v ollama &> /dev/null; then
        OLLAMA_VERSION=$(ollama --version 2>/dev/null || echo "unknown")
        print_success "Ollama already installed: $OLLAMA_VERSION ✓"
        return 0
    fi
    
    print_status "Downloading Ollama installer..."
    curl -fsSL https://ollama.ai/install.sh -o install_ollama.sh &
    spin $!
    
    print_status "Installing Ollama..."
    bash install_ollama.sh
    rm install_ollama.sh
    
    print_success "Ollama installed successfully ✓"
}

# Start Ollama service
start_ollama_service() {
    show_step "Starting Ollama Service"
    
    # Check if already running
    if pgrep -f "ollama serve" > /dev/null; then
        print_success "Ollama service already running ✓"
        return 0
    fi
    
    # Start service
    print_status "Starting Ollama service..."
    nohup ollama serve > ollama.log 2>&1 &
    OLLAMA_PID=$!
    
    # Wait for service to be ready
    print_status "Waiting for service to start..."
    local attempts=0
    while [ $attempts -lt 30 ]; do
        if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
            print_success "Ollama service started successfully ✓"
            return 0
        fi
        sleep 1
        attempts=$((attempts + 1))
    done
    
    print_error "Ollama service failed to start"
    exit 1
}

# Download Qwen model
download_qwen_model() {
    show_step "Downloading Qwen2.5 7B Model"
    
    print_info "Model: qwen2.5:7b-instruct-q4_K_M"
    print_info "Size: 4.7GB (this will take 5-20 minutes)"
    
    # Check if already exists
    if ollama list 2>/dev/null | grep -q "qwen2.5:7b-instruct-q4_K_M"; then
        print_success "Qwen2.5 model already installed ✓"
        return 0
    fi
    
    # Download model
    print_status "Downloading model..."
    ollama pull qwen2.5:7b-instruct-q4_K_M
    
    print_success "Qwen2.5 model ready ✓"
}

# Configure Jupyter
configure_jupyter() {
    show_step "Configuring Jupyter Environment"
    
    # Install Jupyter kernel
    print_status "Installing IPython kernel..."
    python -m ipykernel install --user --name agent_env --display-name "AgentStarterKit"
    
    # Configure Jupyter settings
    print_status "Configuring Jupyter settings..."
    mkdir -p ~/.jupyter
    
    # Create Jupyter config if not exists
    if [ ! -f ~/.jupyter/jupyter_lab_config.py ]; then
        jupyter lab --generate-config 2>/dev/null || true
    fi
    
    # Enable extensions
    print_status "Enabling Jupyter extensions..."
    jupyter labextension install @jupyter-widgets/jupyterlab-manager 2>/dev/null || true
    
    print_success "Jupyter configured ✓"
}

# Create project structure and files
create_project_structure() {
    show_step "Creating Project Structure"
    
    # Create directories
    print_status "Creating directories..."
    mkdir -p agent_workspace
    mkdir -p shared_utils
    mkdir -p logs
    mkdir -p data
    
    # Create .env template
    print_status "Creating environment configuration..."
    cat > .env << 'EOF'
# API Keys (add your keys here)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=qwen2.5:7b-instruct-q4_K_M

# Agent Configuration
AGENT_WORKSPACE=./agent_workspace
LOG_LEVEL=INFO
MAX_ITERATIONS=10
TEMPERATURE=0.7

# Optional Services
DATABASE_URL=sqlite:///agent_data.db
REDIS_URL=redis://localhost:6379
EOF

    # Create quick start script
    print_status "Creating quick start script..."
    cat > start.sh << 'EOF'
#!/bin/bash
# Quick start script for AgentStarterKit

echo "🚀 Starting AgentStarterKit..."

# Activate virtual environment
source agent_env/bin/activate

# Ensure Ollama is running
if ! pgrep -f "ollama serve" > /dev/null; then
    echo "Starting Ollama service..."
    nohup ollama serve > ollama.log 2>&1 &
    sleep 5
fi

# Launch Jupyter Lab
echo "Launching Jupyter Lab..."
jupyter lab --no-browser --port=8888 &

# Wait a moment
sleep 3

# Open in browser
if [[ "$OSTYPE" == "darwin"* ]]; then
    open http://localhost:8888
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open http://localhost:8888 2>/dev/null || echo "Open http://localhost:8888 in your browser"
fi

echo "✅ AgentStarterKit is running!"
echo "📚 Start with: chapter_1/01_what_is_an_agent.ipynb"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user to stop
wait
EOF
    chmod +x start.sh
    
    # Create stop script
    cat > stop.sh << 'EOF'
#!/bin/bash
# Stop all AgentStarterKit services

echo "🛑 Stopping AgentStarterKit services..."

# Stop Jupyter
pkill -f jupyter-lab

# Stop Ollama
pkill -f "ollama serve"

echo "✅ All services stopped"
EOF
    chmod +x stop.sh
    
    # Create utils init
    touch shared_utils/__init__.py
    
    print_success "Project structure created ✓"
}

# Final setup and launch
final_setup() {
    show_step "Final Setup & Launch"
    
    # Create welcome notebook
    print_status "Creating welcome notebook..."
    cat > welcome.ipynb << 'EOF'
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🎉 Welcome to AgentStarterKit!\n",
    "\n",
    "Your environment is fully set up and ready for agent development.\n",
    "\n",
    "## ✅ What's Installed\n",
    "\n",
    "- **Python Environment**: Virtual environment with all dependencies\n",
    "- **Ollama**: Running on http://localhost:11434\n",
    "- **Qwen2.5 7B**: Optimized for function calling (92% accuracy)\n",
    "- **Jupyter Lab**: This interface you're using now\n",
    "\n",
    "## 🚀 Quick Start\n",
    "\n",
    "1. **Start Here**: Open `chapter_1/01_what_is_an_agent.ipynb`\n",
    "2. **Follow the Curriculum**: Work through chapters 1-4 sequentially\n",
    "3. **Experiment**: Each notebook has exercises and challenges\n",
    "\n",
    "## 🔧 Useful Commands\n",
    "\n",
    "- **Start Everything**: `./start.sh`\n",
    "- **Stop Everything**: `./stop.sh`\n",
    "- **Test Ollama**: Run the cell below\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Test Ollama Connection\n",
    "import requests\n",
    "\n",
    "try:\n",
    "    response = requests.get('http://localhost:11434/api/tags')\n",
    "    models = response.json()['models']\n",
    "    print(\"✅ Ollama is running!\")\n",
    "    print(f\"\\nAvailable models:\")\n",
    "    for model in models:\n",
    "        print(f\"  • {model['name']}\")\n",
    "except:\n",
    "    print(\"❌ Ollama not running. Run: ./start.sh\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Quick Model Test\n",
    "import json\n",
    "\n",
    "def test_qwen():\n",
    "    url = 'http://localhost:11434/api/generate'\n",
    "    prompt = \"Hello! Respond with exactly: 'Qwen2.5 ready for agents!'\"\n",
    "    \n",
    "    response = requests.post(url, json={\n",
    "        'model': 'qwen2.5:7b-instruct-q4_K_M',\n",
    "        'prompt': prompt,\n",
    "        'stream': False\n",
    "    })\n",
    "    \n",
    "    result = response.json()['response']\n",
    "    print(f\"Model response: {result}\")\n",
    "\n",
    "test_qwen()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "AgentStarterKit",
   "language": "python",
   "name": "agent_env"
  },
  "language_info": {
   "name": "python",
   "version": "3.8.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
EOF

    # Test final setup
    print_status "Running final tests..."
    python -c "import requests; print('✓ Python packages working')" 2>/dev/null || print_warning "Some packages may need attention"
    
    print_success "Setup complete! 🎉"
}

# Launch Jupyter Lab
launch_jupyter() {
    echo ""
    echo -e "${GREEN}${BOLD}🎊 Installation Complete!${NC}"
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${BOLD}Your AgentStarterKit is ready!${NC}"
    echo ""
    echo -e "${CYAN}Quick Commands:${NC}"
    echo -e "  ${GREEN}./start.sh${NC}  - Start everything (Ollama + Jupyter)"
    echo -e "  ${GREEN}./stop.sh${NC}   - Stop all services"
    echo ""
    echo -e "${CYAN}Manual Start:${NC}"
    echo -e "  ${GREEN}source agent_env/bin/activate${NC}  - Activate environment"
    echo -e "  ${GREEN}jupyter lab${NC}                    - Start Jupyter"
    echo ""
    
    # Ask to launch
    echo -e "${YELLOW}${BOLD}Launch Jupyter Lab now?${NC} [Y/n]: \c"
    read -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
        echo ""
        print_info "Launching Jupyter Lab..."
        
        # Ensure Ollama is still running
        if ! pgrep -f "ollama serve" > /dev/null; then
            nohup ollama serve > ollama.log 2>&1 &
            sleep 3
        fi
        
        # Launch Jupyter
        print_info "Jupyter Lab starting on http://localhost:8888"
        print_info "Opening welcome.ipynb..."
        
        # Start Jupyter in background
        nohup jupyter lab --no-browser --port=8888 welcome.ipynb > jupyter.log 2>&1 &
        JUPYTER_PID=$!
        
        # Wait for Jupyter to start
        sleep 5
        
        # Open browser
        if [[ "$OSTYPE" == "darwin"* ]]; then
            open http://localhost:8888
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            xdg-open http://localhost:8888 2>/dev/null || print_info "Open http://localhost:8888 in your browser"
        fi
        
        echo ""
        print_success "Jupyter Lab is running!"
        print_info "Start with: chapter_1/01_what_is_an_agent.ipynb"
        echo ""
        print_info "Press Ctrl+C to stop all services"
        
        # Keep script running
        trap "pkill -f jupyter-lab; pkill -f 'ollama serve'; exit" INT
        wait $JUPYTER_PID
    else
        echo ""
        print_info "To start later, run: ./start.sh"
    fi
}

# Main installation flow
main() {
    clear
    show_banner
    
    # Pre-flight checks
    check_python
    check_system_requirements
    
    # Core installation
    setup_virtual_environment
    install_python_dependencies
    install_ollama
    start_ollama_service
    download_qwen_model
    
    # Configuration
    configure_jupyter
    create_project_structure
    final_setup
    
    # Launch
    launch_jupyter
}

# Run main installation
main "$@"