# 🤖 AgentStarterKit: Building Autonomous AI Systems

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Status-Active-success.svg" alt="Status">
  <img src="https://img.shields.io/badge/Notebooks-10+-orange.svg" alt="Notebooks">
</p>

<p align="center">
  <strong>A comprehensive, hands-on curriculum for mastering autonomous AI agent development</strong>
</p>

---

## 🎯 Course Overview

Welcome to **AgentStarterKit** - a professional training curriculum designed to take you from AI fundamentals to building sophisticated autonomous agents. Inspired by deeplearning.ai's pedagogical approach, this course emphasizes practical implementation with 70% hands-on coding and 30% conceptual learning.

### What You'll Learn

- **Foundational Concepts**: Understand what makes an AI system truly "agentic"
- **Core Patterns**: Master ReAct, ReWOO, Reflexion, and advanced reasoning paradigms
- **Memory Systems**: Build agents that learn and improve from experience
- **Tool Integration**: Connect agents to real-world APIs, databases, and services
- **Planning & Goals**: Implement hierarchical task planning and goal decomposition
- **Production Skills**: Deploy robust, error-resilient autonomous systems

### Course Philosophy

This curriculum follows a **progressive complexity model** where each module builds upon the previous, ensuring a smooth learning curve from basic concepts to advanced implementations. Every concept is introduced with:
- Clear theoretical foundations
- Working code examples
- Hands-on exercises
- Real-world applications

---

## 🚀 Quick Start

### One-Command Setup

```bash
# Clone the repository
git clone https://github.com/arunmenon/AgentStarterKit.git
cd AgentStarterKit

# Run the zero-friction installer
./install.sh
```

The installer automatically:
- ✅ Sets up Python virtual environment
- ✅ Installs all dependencies
- ✅ Configures Ollama with Qwen2.5 model
- ✅ Sets up Jupyter environment
- ✅ Launches Jupyter with welcome notebook

### Manual Setup (Alternative)

<details>
<summary>Click for manual setup instructions</summary>

```bash
# 1. Create virtual environment
python -m venv agent_env
source agent_env/bin/activate  # On Windows: agent_env\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install Ollama (for local LLM)
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull qwen2.5:7b-instruct

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# 5. Launch Jupyter
jupyter lab
```
</details>

---

## 📚 Course Structure

### Chapter 1: Agent Foundations (3.5 hours)
*From basic concepts to production-ready agents*

| Notebook | Duration | Topics Covered |
|----------|----------|----------------|
| **01_what_is_an_agent.ipynb** | 30 min | • Agent definition and characteristics<br>• Autonomous vs traditional systems<br>• Core components: Perception, Reasoning, Action<br>• Real-world applications |
| **01_agent_foundations.ipynb** | 45 min | • Building your first agent<br>• State management patterns<br>• Basic tool integration<br>• Error handling fundamentals |
| **02_react_pattern.ipynb** | 30 min | • ReAct (Reasoning + Acting) framework<br>• Thought-Action-Observation loops<br>• Implementation best practices<br>• Common pitfalls and solutions |
| **03_react_vs_rewoo.ipynb** | 25 min | • ReWOO (Reasoning Without Observation)<br>• Comparative analysis with ReAct<br>• When to use each pattern<br>• Performance optimization |
| **04_reflexion_pattern.ipynb** | 30 min | • Self-reflection mechanisms<br>• Learning from failures<br>• Iterative improvement<br>• Memory integration |
| **05_advanced_prompting.ipynb** | 40 min | • 58 research-backed techniques<br>• Chain-of-Thought variants<br>• Self-consistency methods<br>• Prompt optimization |
| **06_reasoning_paradigms.ipynb** | 35 min | • Multi-agent debate<br>• Self-verification chains<br>• Recursive reasoning<br>• Ensemble methods |
| **07_evaluation_basics.ipynb** | 25 min | • Agent performance metrics<br>• Evaluation frameworks<br>• A/B testing strategies<br>• Continuous improvement |

### Chapter 2: Memory and Learning (50 min)
*Building agents that remember and improve*

| Notebook | Duration | Topics Covered |
|----------|----------|----------------|
| **02_memory_and_learning.ipynb** | 50 min | • Multi-tier memory architecture<br>• Working memory for immediate context<br>• Episodic memory for experiences<br>• Semantic memory for knowledge<br>• Procedural memory for skills<br>• Experience replay mechanisms<br>• Performance tracking systems |

### Chapter 3: Tool Integration (55 min)
*Connecting agents to the real world*

| Notebook | Duration | Topics Covered |
|----------|----------|----------------|
| **03_tool_integration_and_environment.ipynb** | 55 min | • Production tool frameworks<br>• Database connectivity (SQLite)<br>• Web API integration<br>• File system operations<br>• Error handling & validation<br>• Security best practices<br>• Workflow orchestration |

### Chapter 4: Planning and Goals (60 min)
*Advanced autonomous behavior*

| Notebook | Duration | Topics Covered |
|----------|----------|----------------|
| **04_planning_and_goals.ipynb** | 60 min | • Hierarchical Task Networks<br>• Goal decomposition strategies<br>• Plan execution & monitoring<br>• Adaptive replanning<br>• Multi-goal optimization<br>• Resource management<br>• Complex workflow automation |

---

## 🎓 Learning Path

### Recommended Progression

```mermaid
graph LR
    A[Start] --> B[What is an Agent?]
    B --> C[Agent Foundations]
    C --> D[ReAct Pattern]
    D --> E[ReAct vs ReWOO]
    E --> F[Reflexion Pattern]
    F --> G[Advanced Prompting]
    G --> H[Reasoning Paradigms]
    H --> I[Evaluation Basics]
    I --> J[Memory & Learning]
    J --> K[Tool Integration]
    K --> L[Planning & Goals]
    L --> M[Build Your Own Agent!]
```

### Prerequisites

- **Python**: Intermediate knowledge (functions, classes, async/await)
- **Machine Learning**: Basic understanding of LLMs and prompting
- **Development**: Familiarity with Jupyter notebooks and Git

### Time Commitment

- **Total Duration**: ~5 hours of core content
- **Exercises**: Additional 3-5 hours
- **Projects**: 5-10 hours for capstone project

---

## 🛠️ Technical Stack

### Core Technologies
- **Python 3.8+**: Primary programming language
- **OpenAI API**: For GPT model access
- **Ollama**: Local LLM deployment (Qwen2.5)
- **Jupyter Lab**: Interactive development environment

### Key Libraries
```python
# AI/ML
openai>=1.0.0        # OpenAI API client
anthropic>=0.3.0     # Anthropic API (optional)

# Data & Visualization
numpy>=1.24.0        # Numerical computing
pandas>=2.0.0        # Data manipulation
matplotlib>=3.7.0    # Plotting
seaborn>=0.12.0     # Statistical visualization

# Tools & Integration
requests>=2.31.0     # HTTP client
python-dotenv>=1.0.0 # Environment management
networkx>=3.1.0      # Graph algorithms for planning
```

---

## 💡 Key Features

### 🔄 Progressive Complexity
Each module builds on previous concepts, ensuring smooth skill development

### 🛡️ Production-Ready Code
Learn patterns and practices used in real autonomous systems

### 🎯 Hands-On Focus
70% practical coding with immediate feedback

### 🧪 Extensive Examples
Every concept illustrated with working code

### 📊 Performance Metrics
Built-in evaluation tools to measure agent effectiveness

### 🔧 Debugging Tools
Comprehensive error handling and debugging techniques

---

## 🏆 Learning Outcomes

By completing this curriculum, you will be able to:

1. **Design and implement** autonomous agents using state-of-the-art patterns
2. **Build memory systems** that enable continuous learning
3. **Integrate real-world tools** with proper error handling
4. **Create hierarchical planners** for complex task automation
5. **Evaluate and optimize** agent performance systematically
6. **Deploy production-ready** autonomous systems

---

## 📖 Additional Resources

### Recommended Reading
- [Anthropic's Constitutional AI](https://www.anthropic.com/constitutional.pdf)
- [ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629)
- [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)

### Community
- 💬 [Discord Server](https://discord.gg/agentstartkit)
- 🐦 [Twitter Updates](https://twitter.com/agentstartkit)
- 📧 [Newsletter](https://agentstartkit.substack.com)

---

<p align="center">
  <strong>Start your journey in autonomous AI development today!</strong><br>
  <em>Questions? Open an issue or reach out on Discord.</em>
</p>