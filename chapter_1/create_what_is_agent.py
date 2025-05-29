#!/usr/bin/env python3
"""Create the 01_what_is_an_agent.ipynb notebook"""

import json

notebook_content = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Module 1.1: What is an AI Agent?\n",
                "\n",
                "**Duration**: 15 minutes\n",
                "**Level**: Foundation\n",
                "\n",
                "## 🎯 Learning Objectives\n",
                "\n",
                "By the end of this notebook, you will:\n",
                "- Understand the spectrum from reactive to agentic AI systems\n",
                "- Identify the 5 key properties that make a system \"agentic\"\n",
                "- Trace the evolution of agent architectures (2023-2025)\n",
                "- Analyze real systems to determine their level of agency\n",
                "- Design basic agent control loops\n",
                "\n",
                "## 📚 No Prerequisites!\n",
                "\n",
                "This is a conceptual introduction - no coding required. We'll build actual agents in the next notebook."
            ]
        }
    ],
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

# Write the notebook
with open("01_what_is_an_agent.ipynb", "w") as f:
    json.dump(notebook_content, f, indent=2)

print("Created 01_what_is_an_agent.ipynb")

# Now let's create the complete focused notebooks script
import subprocess
import sys

# Create the complete notebooks generation script
complete_script = '''#!/usr/bin/env python3
"""Create all focused Module 1 notebooks with cutting-edge agent theory"""

import json
import os

def create_notebook(filename, cells):
    """Create a properly formatted Jupyter notebook"""
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python", 
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    # Ensure all cells have required fields
    for cell in notebook["cells"]:
        if "execution_count" not in cell:
            cell["execution_count"] = None
        if "metadata" not in cell:
            cell["metadata"] = {}
        if cell["cell_type"] == "code" and "outputs" not in cell:
            cell["outputs"] = []
    
    with open(filename, "w") as f:
        json.dump(notebook, f, indent=2)
    print(f"Created: {filename}")

# Create all 7 notebooks
print("Creating Module 1 focused notebooks...")

# Notebook 2: ReAct Pattern (Full implementation)
notebook2_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Module 1.2: The ReAct Pattern Implementation\\n",
            "\\n",
            "**Duration**: 30 minutes\\n",
            "**Level**: Foundation\\n",
            "\\n",
            "Build a complete ReAct agent from scratch!"
        ]
    },
    {
        "cell_type": "code", 
        "metadata": {},
        "source": [
            "# ReAct implementation will go here\\n",
            "print(\\"ReAct Pattern Notebook\\")"
        ]
    }
]

# Notebook 3: ReAct vs ReWOO
notebook3_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Module 1.3: ReAct vs ReWOO - 64% Token Reduction\\n",
            "\\n",
            "Compare and implement both patterns."
        ]
    }
]

# Notebook 4: Reflexion
notebook4_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Module 1.4: Reflexion - Verbal Reinforcement Learning\\n",
            "\\n",
            "91% accuracy through self-reflection."
        ]
    }
]

# Notebook 5: Advanced Prompting
notebook5_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Module 1.5: Advanced Prompting (2024-2025)\\n",
            "\\n",
            "58 techniques from cutting-edge research."
        ]
    }
]

# Notebook 6: Reasoning Paradigms
notebook6_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Module 1.6: From CoT to ToT\\n",
            "\\n",
            "Evolution of reasoning patterns."
        ]
    }
]

# Notebook 7: Evaluation
notebook7_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Module 1.7: Benchmarking Agents\\n",
            "\\n",
            "τ-bench principles and reality check."
        ]
    }
]

# Create all notebooks
create_notebook("02_react_pattern.ipynb", notebook2_cells)
create_notebook("03_react_vs_rewoo.ipynb", notebook3_cells)
create_notebook("04_reflexion_pattern.ipynb", notebook4_cells)
create_notebook("05_advanced_prompting.ipynb", notebook5_cells)
create_notebook("06_reasoning_paradigms.ipynb", notebook6_cells)
create_notebook("07_evaluation_basics.ipynb", notebook7_cells)

print("\\n✅ All notebooks created successfully!")
'''

# Write the complete script
with open("create_all_notebooks.py", "w") as f:
    f.write(complete_script)

print("\n✅ Created create_all_notebooks.py")
print("Running it now...")

# Run the script
subprocess.run([sys.executable, "create_all_notebooks.py"])