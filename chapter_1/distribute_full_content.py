#!/usr/bin/env python3
"""Distribute full content from original notebook to focused notebooks"""

import json
import os

# Read the original advanced notebook
with open('01_agent_foundations_advanced.ipynb', 'r') as f:
    original = json.load(f)

# Extract cells by topic
environment_cells = []
react_cells = []
tool_cells = []
demo_cells = []

for i, cell in enumerate(original['cells']):
    if cell['cell_type'] == 'markdown':
        content = ''.join(cell['source'])
        if 'Environment Setup' in content:
            environment_cells.append(cell)
        elif 'ReAct Pattern' in content:
            react_cells.append(cell)
        elif 'Building Tools' in content:
            tool_cells.append(cell)
    elif cell['cell_type'] == 'code':
        # Extract code cells following the topics
        if i > 0:
            prev_cell = original['cells'][i-1]
            if prev_cell['cell_type'] == 'markdown':
                prev_content = ''.join(prev_cell['source'])
                if 'LLM Integration' in prev_content or 'OllamaLLM' in ''.join(cell['source']):
                    react_cells.append(cell)
                elif 'Tool' in ''.join(cell['source']) or 'SearchTool' in ''.join(cell['source']):
                    tool_cells.append(cell)
                elif 'Demo' in prev_content or 'agent.run' in ''.join(cell['source']):
                    demo_cells.append(cell)

# Now create enhanced notebooks with full content

# Notebook 2: Full ReAct Pattern Implementation
notebook2_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": ["# Module 1.2: The ReAct Pattern - Complete Implementation 🔄\n\n**Duration**: 30 minutes  \n**Level**: Foundation  \n\n## 🎯 Learning Objectives\n\n- Build a complete ReAct agent from scratch\n- Understand Think → Act → Observe loop\n- Implement tool integration\n- Debug agent behavior\n- Measure performance\n\n---"]
    }
]

# Add environment setup
notebook2_cells.extend(environment_cells[:2])  # Setup cells

# Add all ReAct implementation cells
notebook2_cells.extend(react_cells)

# Add tool implementation
notebook2_cells.extend(tool_cells)

# Add demo cells
notebook2_cells.extend(demo_cells)

# Save notebook 2
def save_notebook(filename, cells):
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    for cell in notebook["cells"]:
        if "execution_count" not in cell:
            cell["execution_count"] = None
        if "metadata" not in cell:
            cell["metadata"] = {}
        if cell["cell_type"] == "code" and "outputs" not in cell:
            cell["outputs"] = []
    
    with open(filename, 'w') as f:
        json.dump(notebook, f, indent=2)
    print(f"Created: {filename}")

save_notebook("02_react_pattern_complete.ipynb", notebook2_cells)

print("✅ Distributed ReAct implementation to notebook 2")
print(f"   Added {len(notebook2_cells)} cells")
print("\nNext: Create ReWOO, Reflexion implementations...")