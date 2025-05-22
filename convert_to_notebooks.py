#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

def convert_python_to_notebook(python_file_path, output_path):
    """Convert a Python file to a Jupyter notebook."""
    
    with open(python_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content into cells based on markdown comments and code blocks
    cells = []
    
    # Split by triple quotes (markdown sections) and code sections
    parts = re.split(r'("""[\s\S]*?""")', content)
    
    for i, part in enumerate(parts):
        part = part.strip()
        if not part:
            continue
            
        if part.startswith('"""') and part.endswith('"""'):
            # This is a markdown cell
            markdown_content = part[3:-3].strip()
            if markdown_content:
                cell = {
                    "cell_type": "markdown",
                    "id": f"markdown-{i}",
                    "metadata": {},
                    "source": markdown_content.split('\n')
                }
                cells.append(cell)
        else:
            # This is a code cell
            if part:
                cell = {
                    "cell_type": "code",
                    "execution_count": None,
                    "id": f"code-{i}",
                    "metadata": {},
                    "outputs": [],
                    "source": part.split('\n')
                }
                cells.append(cell)
    
    # Create notebook structure
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }
    
    # Write notebook file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    
    print(f"Converted {python_file_path} to {output_path}")

if __name__ == "__main__":
    conversions = [
        ("/Users/arunmenon/Downloads/module_01_notebook.py", "/Users/arunmenon/projects/AgentStarterKit/chapter_1/01_agent_foundations.ipynb"),
        ("/Users/arunmenon/Downloads/module_02_notebook.py", "/Users/arunmenon/projects/AgentStarterKit/chapter_2/02_memory_and_learning.ipynb"),
        ("/Users/arunmenon/Downloads/module_03_notebook.py", "/Users/arunmenon/projects/AgentStarterKit/chapter_3/03_tool_integration_and_environment.ipynb"),
        ("/Users/arunmenon/Downloads/module_04_notebook.py", "/Users/arunmenon/projects/AgentStarterKit/chapter_4/04_planning_and_goals.ipynb"),
    ]
    
    for python_file, notebook_file in conversions:
        if Path(python_file).exists():
            convert_python_to_notebook(python_file, notebook_file)
        else:
            print(f"Warning: {python_file} not found")