#!/bin/bash
# AgentStarterKit Zero-Friction Installer
# Handles all contingencies for a smooth installation experience

set -e

# Colors and formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Progress tracking
CURRENT_STEP=0
TOTAL_STEPS=8

# Installation state file
STATE_FILE=".install_state"

# Print functions
print_header() {
    clear
    echo -e "${CYAN}"
    cat << "EOF"
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
    echo
}

print_error() {
    echo -e "${RED}  ❌${NC} $1"
}

print_success() {
    echo -e "${GREEN}  ✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}  ⚠️${NC} $1"
}

print_info() {
    echo -e "${PURPLE}  ℹ️${NC} $1"
}

print_status() {
    echo -e "${BLUE}  ▶${NC} $1"
}

show_step() {
    CURRENT_STEP=$((CURRENT_STEP + 1))
    echo
    echo -e "${BLUE}[${CURRENT_STEP}/${TOTAL_STEPS}]${NC} ${BOLD}$1${NC}"
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Spinner for long operations
spin() {
    local pid=$1
    local delay=0.1
    local spinstr='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

# State management
save_state() {
    echo "$1" > "$STATE_FILE"
}

get_state() {
    if [ -f "$STATE_FILE" ]; then
        cat "$STATE_FILE"
    else
        echo "none"
    fi
}

clear_state() {
    rm -f "$STATE_FILE"
}

# Detect Python command
detect_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        return 1
    fi
    return 0
}

# Check Python version
check_python() {
    show_step "Checking Python Installation"
    
    if ! detect_python; then
        print_error "Python not found!"
        print_info "Please install Python 3.8+ from https://python.org"
        exit 1
    fi
    
    print_info "Found Python: $PYTHON_CMD (version $(${PYTHON_CMD} --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2))"
    
    # Check version
    PYTHON_VERSION=$(${PYTHON_CMD} -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    if (( $(echo "$PYTHON_VERSION < 3.8" | bc -l) )); then
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
    
    # Check if environment exists
    if [ -d "agent_env" ]; then
        print_warning "Virtual environment 'agent_env' already exists"
        
        # Try to activate it
        if [ -f "agent_env/bin/activate" ]; then
            print_status "Testing existing environment..."
            if source agent_env/bin/activate 2>/dev/null && python --version &>/dev/null; then
                print_success "Existing environment is valid and will be used ✓"
                
                # Upgrade pip in existing environment
                print_status "Upgrading pip..."
                pip install --upgrade pip --quiet
                return 0
            else
                print_warning "Existing environment appears corrupted"
            fi
        fi
        
        # Ask to recreate
        echo -e "${YELLOW}  ┌─────────────────────────────────────────────────┐${NC}"
        echo -e "${YELLOW}  │ Options:                                        │${NC}"
        echo -e "${YELLOW}  │ [1] Use existing environment (default)          │${NC}"
        echo -e "${YELLOW}  │ [2] Recreate fresh environment                  │${NC}"
        echo -e "${YELLOW}  │ [3] Cancel installation                         │${NC}"
        echo -e "${YELLOW}  └─────────────────────────────────────────────────┘${NC}"
        
        read -p "  Choose option [1-3]: " -n 1 -r choice
        echo
        
        case "$choice" in
            2)
                print_status "Removing old environment..."
                rm -rf agent_env
                ;;
            3)
                print_info "Installation cancelled"
                exit 0
                ;;
            *)
                print_info "Using existing environment"
                source agent_env/bin/activate
                return 0
                ;;
        esac
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
    save_state "venv_created"
}

# Install Python dependencies
install_python_dependencies() {
    show_step "Installing Python Dependencies"
    
    # Check if already installed
    if [ -f "requirements.txt" ] && pip freeze | grep -q "jupyter"; then
        print_status "Checking installed packages..."
        
        # Quick check for core packages
        local missing_packages=0
        for package in jupyter pandas numpy matplotlib requests; do
            if ! pip show $package &>/dev/null; then
                missing_packages=$((missing_packages + 1))
            fi
        done
        
        if [ $missing_packages -eq 0 ]; then
            print_success "Core packages already installed ✓"
            print_info "Run 'pip install -r requirements.txt' to update packages"
            return 0
        else
            print_warning "Some packages missing, reinstalling..."
        fi
    fi
    
    # Create comprehensive requirements.txt if it doesn't exist or is outdated
    print_status "Updating requirements.txt..."
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
websockets>=10.4

# Database & Storage
sqlalchemy>=2.0.0
redis>=4.5.0

# Utilities
python-dotenv>=0.21.0
pydantic>=1.10.0
typer>=0.7.0
loguru>=0.6.0

# Jupyter & Development
jupyter>=1.0.0
jupyterlab>=3.5.0
notebook>=6.5.0
ipykernel>=6.19.0
ipywidgets>=8.0.0
nbformat>=5.7.0

# Planning & Algorithms
networkx>=3.0

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
    
    # Install in batches for better error handling
    pip install --upgrade pip setuptools wheel --quiet
    
    # Core packages first
    print_status "Installing core packages..."
    pip install jupyter jupyterlab notebook ipykernel --quiet --progress-bar on
    
    # Then all others
    print_status "Installing remaining packages..."
    pip install -r requirements.txt --quiet --progress-bar on
    
    print_success "All Python packages installed ✓"
    save_state "packages_installed"
}

# Install and configure Ollama
install_ollama() {
    show_step "Installing Ollama"
    
    # Check if already installed
    if command -v ollama &> /dev/null; then
        OLLAMA_VERSION=$(ollama --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || echo "unknown")
        print_success "Ollama already installed (version: $OLLAMA_VERSION) ✓"
        
        # Check if it's working
        print_status "Testing Ollama installation..."
        if ollama list &>/dev/null; then
            print_success "Ollama is working correctly ✓"
            return 0
        else
            print_warning "Ollama installed but not responding, attempting fix..."
        fi
    fi
    
    # Install Ollama
    print_status "Downloading Ollama installer..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS installation
        if ! command -v brew &> /dev/null; then
            # Direct installation
            curl -fsSL https://ollama.ai/install.sh -o install_ollama.sh &
            spin $!
            
            print_status "Installing Ollama..."
            bash install_ollama.sh
            rm install_ollama.sh
        else
            # Use Homebrew if available
            print_status "Installing Ollama via Homebrew..."
            brew install ollama
        fi
    else
        # Linux installation
        curl -fsSL https://ollama.ai/install.sh -o install_ollama.sh &
        spin $!
        
        print_status "Installing Ollama..."
        bash install_ollama.sh
        rm install_ollama.sh
    fi
    
    # Verify installation
    if command -v ollama &> /dev/null; then
        print_success "Ollama installed successfully ✓"
    else
        print_error "Ollama installation failed"
        print_info "Please install manually from https://ollama.ai"
        exit 1
    fi
    
    save_state "ollama_installed"
}

# Start Ollama service
start_ollama_service() {
    show_step "Starting Ollama Service"
    
    # Check if already running
    if pgrep -f "ollama serve" > /dev/null; then
        print_success "Ollama service already running ✓"
        
        # Verify it's responding
        if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
            return 0
        else
            print_warning "Service running but not responding, restarting..."
            pkill -f "ollama serve"
            sleep 2
        fi
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
            save_state "ollama_started"
            return 0
        fi
        sleep 1
        attempts=$((attempts + 1))
        printf "."
    done
    
    print_error "Ollama service failed to start"
    print_info "Check ollama.log for details"
    exit 1
}

# Download Qwen model
download_qwen_model() {
    show_step "Downloading Qwen2.5 7B Model"
    
    print_info "Model: qwen2.5:7b-instruct-q4_K_M"
    print_info "Size: ~4.7GB"
    
    # Check if already exists
    print_status "Checking for existing model..."
    if ollama list 2>/dev/null | grep -q "qwen2.5:7b-instruct-q4_K_M"; then
        print_success "Qwen2.5 model already installed ✓"
        
        # Test the model
        print_status "Testing model..."
        if echo "Hello" | ollama run qwen2.5:7b-instruct-q4_K_M --verbose 2>/dev/null | grep -q "Hello"; then
            print_success "Model is working correctly ✓"
            return 0
        else
            print_warning "Model exists but not responding, re-downloading..."
            ollama rm qwen2.5:7b-instruct-q4_K_M 2>/dev/null || true
        fi
    fi
    
    # Check disk space
    print_status "Checking available disk space..."
    AVAILABLE_SPACE_GB=$(df . | awk 'NR==2 {print int($4/1024/1024)}')
    if [ "$AVAILABLE_SPACE_GB" -lt 6 ]; then
        print_error "Insufficient disk space for model: ${AVAILABLE_SPACE_GB}GB available, 6GB required"
        print_info "Free up disk space and run installer again"
        exit 1
    fi
    
    # Download model with progress
    print_status "Downloading model (this may take 5-20 minutes)..."
    print_info "Download speed depends on your internet connection"
    
    if ! ollama pull qwen2.5:7b-instruct-q4_K_M; then
        print_error "Model download failed"
        print_info "Possible causes:"
        print_info "  - Internet connection interrupted"
        print_info "  - Ollama service not running"
        print_info "  - Insufficient disk space"
        print_info "Run installer again to retry"
        exit 1
    fi
    
    print_success "Qwen2.5 model ready ✓"
    save_state "model_downloaded"
}

# Configure Jupyter
configure_jupyter() {
    show_step "Configuring Jupyter Environment"
    
    # Install Jupyter kernel
    print_status "Installing IPython kernel..."
    python -m ipykernel install --user --name agent_env --display-name "AgentStarterKit" 2>/dev/null || {
        print_warning "Kernel installation requires sudo, trying with --user flag..."
        python -m ipykernel install --user --name agent_env --display-name "AgentStarterKit"
    }
    
    # Configure Jupyter settings
    print_status "Configuring Jupyter settings..."
    mkdir -p ~/.jupyter
    
    # Create Jupyter config if not exists
    if [ ! -f ~/.jupyter/jupyter_lab_config.py ]; then
        jupyter lab --generate-config 2>/dev/null || true
    fi
    
    # Enable extensions (if supported)
    print_status "Setting up Jupyter extensions..."
    jupyter labextension list 2>/dev/null || true
    
    print_success "Jupyter configured ✓"
    save_state "jupyter_configured"
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
    
    # Create .env template if not exists
    if [ ! -f ".env" ]; then
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
EOF
        print_info "Created .env file - add your API keys when ready"
    else
        print_info ".env file already exists ✓"
    fi
    
    # Create quick start script
    print_status "Creating quick start script..."
    cat > start_jupyter.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting AgentStarterKit Environment..."

# Activate virtual environment
source agent_env/bin/activate

# Start Ollama if not running
if ! pgrep -f "ollama serve" > /dev/null; then
    echo "Starting Ollama service..."
    nohup ollama serve > ollama.log 2>&1 &
    sleep 3
fi

# Launch Jupyter
echo "Launching Jupyter Lab..."
jupyter lab --NotebookApp.token='' --NotebookApp.password=''
EOF
    chmod +x start_jupyter.sh
    
    # Create stop script
    cat > stop_services.sh << 'EOF'
#!/bin/bash
echo "🛑 Stopping AgentStarterKit Services..."

# Stop Jupyter
echo "Stopping Jupyter..."
jupyter notebook stop 8888 2>/dev/null || true
pkill -f jupyter-lab 2>/dev/null || true

# Stop Ollama
echo "Stopping Ollama..."
pkill -f "ollama serve" 2>/dev/null || true

echo "✅ All services stopped"
EOF
    chmod +x stop_services.sh
    
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
    "Your environment is set up and ready to go. Let's verify everything is working correctly."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Test imports\n",
    "import sys\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import requests\n",
    "from pathlib import Path\n",
    "\n",
    "print(f\"Python version: {sys.version}\")\n",
    "print(f\"Pandas version: {pd.__version__}\")\n",
    "print(f\"NumPy version: {np.__version__}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Test Ollama connection\n",
    "import requests\n",
    "\n",
    "try:\n",
    "    response = requests.get('http://localhost:11434/api/tags')\n",
    "    if response.status_code == 200:\n",
    "        models = response.json()['models']\n",
    "        print(\"✅ Ollama is running!\")\n",
    "        print(f\"Available models: {[m['name'] for m in models]}\")\n",
    "    else:\n",
    "        print(\"❌ Ollama service not responding\")\n",
    "except Exception as e:\n",
    "    print(f\"❌ Could not connect to Ollama: {e}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Test Qwen model\n",
    "import json\n",
    "\n",
    "def test_qwen():\n",
    "    url = \"http://localhost:11434/api/generate\"\n",
    "    payload = {\n",
    "        \"model\": \"qwen2.5:7b-instruct-q4_K_M\",\n",
    "        \"prompt\": \"What is an AI agent in one sentence?\",\n",
    "        \"stream\": False\n",
    "    }\n",
    "    \n",
    "    try:\n",
    "        response = requests.post(url, json=payload)\n",
    "        if response.status_code == 200:\n",
    "            result = response.json()\n",
    "            print(\"✅ Qwen model is working!\")\n",
    "            print(f\"\\nResponse: {result['response']}\")\n",
    "        else:\n",
    "            print(f\"❌ Model error: {response.status_code}\")\n",
    "    except Exception as e:\n",
    "        print(f\"❌ Could not test model: {e}\")\n",
    "\n",
    "test_qwen()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 🚀 Next Steps\n",
    "\n",
    "1. **Start Learning**: Open `chapter_1/01_what_is_an_agent.ipynb`\n",
    "2. **Add API Keys**: Edit `.env` file with your API keys (optional)\n",
    "3. **Explore**: Check out the course structure in the README\n",
    "\n",
    "Happy learning! 🎓"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "AgentStarterKit",
   "language": "python",
   "name": "agent_env"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
EOF
    
    print_success "Project structure created ✓"
    save_state "project_created"
}

# Launch Jupyter
launch_jupyter() {
    echo
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✨ Installation Complete! ✨${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo
    
    # Check if we should launch Jupyter
    echo -e "${CYAN}Ready to start learning?${NC}"
    read -p "Launch Jupyter Lab now? [Y/n]: " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        echo
        echo -e "${YELLOW}To start later, run:${NC}"
        echo -e "${WHITE}  ./start_jupyter.sh${NC}"
        echo
        echo -e "${YELLOW}To stop services:${NC}"
        echo -e "${WHITE}  ./stop_services.sh${NC}"
        echo
        clear_state
        exit 0
    fi
    
    # Launch Jupyter
    print_info "Launching Jupyter Lab..."
    print_info "Browser will open automatically"
    print_info "Press Ctrl+C to stop"
    echo
    
    # Clean state file
    clear_state
    
    # Launch with specific settings
    jupyter lab --NotebookApp.token='' --NotebookApp.password='' --no-browser &
    JUPYTER_PID=$!
    
    # Wait a moment for server to start
    sleep 3
    
    # Open browser
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open http://localhost:8888
    elif command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:8888
    else
        print_info "Open http://localhost:8888 in your browser"
    fi
    
    # Wait for Jupyter process
    wait $JUPYTER_PID
}

# Cleanup on exit
cleanup() {
    if [ -n "$OLLAMA_PID" ]; then
        kill $OLLAMA_PID 2>/dev/null || true
    fi
    clear_state
}

trap cleanup EXIT

# Resume installation from saved state
resume_from_state() {
    local state=$(get_state)
    case "$state" in
        "venv_created")
            print_info "Resuming from virtual environment setup..."
            source agent_env/bin/activate
            CURRENT_STEP=2
            ;;
        "packages_installed")
            print_info "Resuming from package installation..."
            source agent_env/bin/activate
            CURRENT_STEP=3
            ;;
        "ollama_installed")
            print_info "Resuming from Ollama installation..."
            source agent_env/bin/activate
            CURRENT_STEP=4
            ;;
        "ollama_started")
            print_info "Resuming from Ollama service start..."
            source agent_env/bin/activate
            CURRENT_STEP=5
            ;;
        "model_downloaded")
            print_info "Resuming from model download..."
            source agent_env/bin/activate
            CURRENT_STEP=6
            ;;
        "jupyter_configured")
            print_info "Resuming from Jupyter configuration..."
            source agent_env/bin/activate
            CURRENT_STEP=7
            ;;
        "project_created")
            print_info "Installation already complete!"
            source agent_env/bin/activate
            launch_jupyter
            exit 0
            ;;
    esac
}

# Main installation flow
main() {
    print_header
    
    # Check for resume
    if [ -f "$STATE_FILE" ]; then
        print_warning "Previous installation detected"
        read -p "Resume installation? [Y/n]: " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
            resume_from_state
        else
            clear_state
            CURRENT_STEP=0
        fi
    fi
    
    # Run installation steps
    if [ $CURRENT_STEP -lt 1 ]; then check_python; fi
    if [ $CURRENT_STEP -lt 2 ]; then check_system_requirements; fi
    if [ $CURRENT_STEP -lt 3 ]; then setup_virtual_environment; fi
    if [ $CURRENT_STEP -lt 4 ]; then install_python_dependencies; fi
    if [ $CURRENT_STEP -lt 5 ]; then install_ollama; fi
    if [ $CURRENT_STEP -lt 6 ]; then start_ollama_service; fi
    if [ $CURRENT_STEP -lt 7 ]; then download_qwen_model; fi
    if [ $CURRENT_STEP -lt 8 ]; then configure_jupyter; fi
    create_project_structure
    
    # Launch
    launch_jupyter
}

# Run main installation
main