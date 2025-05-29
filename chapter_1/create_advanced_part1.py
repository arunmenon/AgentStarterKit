import json

# Create the notebook structure
notebook = {
    'cells': [],
    'metadata': {
        'kernelspec': {
            'display_name': 'Python 3',
            'language': 'python',
            'name': 'python3'
        }
    },
    'nbformat': 4,
    'nbformat_minor': 4
}

# Helper functions
def add_markdown_cell(content):
    return {
        'cell_type': 'markdown',
        'metadata': {},
        'source': content.split('\n')
    }

def add_code_cell(content):
    return {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': content.split('\n')
    }

# Build cells
cells = []

# Title
cells.append(add_markdown_cell('''# Module 1: Agent Foundations (Advanced)
*Building Autonomous AI Agents from First Principles*

## 🎯 Module Overview

**Duration**: 45 minutes  
**Prerequisites**: Basic Python knowledge

### What You'll Learn
1. Core Agent Theory
2. Agent Architecture  
3. Environment & Perception
4. Goals & Planning
5. ReAct Pattern
6. Performance Metrics'''))

# Add more cells...
notebook['cells'] = cells

# Save
with open('01_agent_foundations_advanced.ipynb', 'w') as f:
    json.dump(notebook, f, indent=2)

print('✅ Created notebook')
