# 🤖 Agent Starter Kit

A comprehensive educational curriculum for building autonomous AI agents from foundations to advanced planning systems.

## 📚 Overview

This curriculum follows a progressive learning approach with **70% hands-on coding** and **30% conceptual learning**. Each module builds upon the previous ones, taking you from basic agent concepts to sophisticated multi-agent applications.

**Total Duration:** ~8 hours of guided learning  
**Format:** Interactive Jupyter notebooks with guided exercises  
**Prerequisites:** Basic Python knowledge, familiarity with APIs  

## 🎯 Learning Objectives

By the end of this curriculum, you will be able to:
- Design and implement autonomous AI agents
- Build sophisticated memory and learning systems
- Create robust tool integration frameworks
- Implement advanced planning and goal decomposition
- Deploy production-ready agentic applications

## 📖 Curriculum Structure

### **Module 1: Agent Foundations** (45 minutes)
**Notebook:** `chapter_1/01_agent_foundations.ipynb`

**What You'll Build:**
- Complete agent architecture with ReAct pattern
- Web search, calculator, and note-taking tools
- Memory system for experience tracking

**Key Concepts:**
- Agent anatomy and components
- ReAct (Reasoning + Acting) pattern
- Tool usage and environment interaction

### **Module 2: Memory and Learning** (50 minutes)
**Notebook:** `chapter_2/02_memory_and_learning.ipynb`

**What You'll Build:**
- Advanced memory architecture (Working, Episodic, Semantic, Procedural)
- Learning agents that improve through experience
- Smart tools that adapt to usage patterns
- User personalization engine

**Key Concepts:**
- Memory types and management
- Experience-based learning
- Context-aware conversations
- Memory consolidation and optimization

### **Module 3: Tool Integration and Environment Interaction** (55 minutes)
**Notebook:** `chapter_3/03_tool_integration_and_environment.ipynb`

**What You'll Build:**
- Production-ready tool framework with error handling
- Database, API, file processing, and email tools
- Advanced tool manager with workflow orchestration
- Intelligent tool recommendation system

**Key Concepts:**
- Robust tool architecture
- Error handling and resilience
- Security and validation
- Workflow coordination

### **Module 4: Planning and Goal Decomposition** (60 minutes)
**Notebook:** `chapter_4/04_planning_and_goals.ipynb`

**What You'll Build:**
- Hierarchical Task Network (HTN) planner
- Goal-Oriented Action Planning (GOAP) system
- Adaptive plan executor with monitoring
- Complex multi-step workflow demonstrations

**Key Concepts:**
- Hierarchical planning systems
- Goal decomposition strategies
- Self-correcting planning mechanisms
- Adaptive execution and replanning

## 🚀 Quick Start

### 1. **Clone the Repository**
```bash
git clone https://github.com/arunmenon/AgentStarterKit.git
cd AgentStarterKit
```

### 2. **Run Setup Script**
```bash
bash setup.sh
```

### 3. **Configure API Keys**
```bash
# Edit the .env file with your API keys
nano .env
```

Add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. **Start Jupyter**
```bash
source agent_env/bin/activate
jupyter lab
```

### 5. **Begin Learning**
Start with `chapter_1/01_agent_foundations.ipynb` and work through the modules sequentially.

## 🛠️ Technical Requirements

### Dependencies
- Python 3.8+
- OpenAI API key (required)
- Internet connection (for API calls and package installation)

### Key Libraries
- `openai` - LLM integration
- `pandas`, `numpy` - Data processing
- `matplotlib`, `seaborn` - Visualization
- `networkx` - Graph algorithms for planning
- `aiohttp`, `requests` - API integration
- `jupyter` - Interactive development

## 📊 Learning Path Recommendations

### **Beginner Path** (First-time with AI agents)
Start with Module 1, focus on understanding basic concepts before moving to advanced systems.

### **Intermediate Path** (Some AI/ML experience)
Begin with Module 1 for agent-specific concepts, then progress through all modules with focus on practical implementations.

### **Advanced Path** (Experienced developers)
Review Modules 1-2 quickly, spend more time on Modules 3-4 with additional challenges and customizations.

## 🔧 Project Structure

```
AgentStarterKit/
├── README.md                     # This file
├── setup.sh                      # Automated setup script
├── requirements.txt               # Python dependencies (auto-generated)
├── .env                          # Environment variables (create from template)
├── .gitignore                    # Git ignore rules
├── chapter_1/
│   └── 01_agent_foundations.ipynb
├── chapter_2/
│   └── 02_memory_and_learning.ipynb
├── chapter_3/
│   └── 03_tool_integration_and_environment.ipynb
├── chapter_4/
│   └── 04_planning_and_goals.ipynb
└── agent_workspace/              # File processing workspace (auto-created)
```

## 💡 Educational Features

### **Hands-On Exercises**
- Guided coding exercises with step-by-step instructions
- Solution reveals for self-checking
- Challenge problems for advanced learners

### **Real-World Examples**
- Database query tools with safety checks
- Web API integration with authentication
- File processing with security validation
- Email communication systems
- Complex workflow orchestration

### **Progressive Complexity**
- Each module builds on previous concepts
- Clear learning objectives and knowledge checks
- Comprehensive progress tracking
- Production-ready code examples

## 🎯 Success Metrics

Students will be considered successful upon:
- Completing all 4 modules with understanding
- Successfully implementing guided exercises
- Demonstrating knowledge through built-in checks
- Building functional agents that can plan and execute complex tasks

## 🔬 Advanced Topics (Optional)

After completing the core curriculum, explore these advanced concepts:

1. **Multi-Agent Communication** - Agents that collaborate
2. **Distributed Agent Systems** - Scalable agent architectures
3. **Agent Safety and Alignment** - Ensuring reliable behavior
4. **Production Deployment** - Scaling agents in real environments

## 🤝 Contributing

This is an educational resource. If you find issues or have improvements:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with clear description

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by DeepLearning.ai's educational methodology
- Built with modern AI agent frameworks and best practices
- Designed for hands-on learning and practical application

---

**Ready to build the future of intelligent automation?** 🚀

Start with `chapter_1/01_agent_foundations.ipynb` and begin your journey into agentic AI systems!