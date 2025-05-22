#!/usr/bin/env python3
import json
import re
from pathlib import Path

def parse_python_notebook(python_file):
    """Parse a Python file and convert it to proper notebook cells"""
    with open(python_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    cells = []
    current_cell = []
    current_type = None
    cell_id = 0
    
    lines = content.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check for triple quote markdown blocks
        if line.strip().startswith('"""') and not line.strip().endswith('"""'):
            # Start of markdown block
            if current_cell and current_type:
                # Save previous cell
                cells.append(create_cell(current_cell, current_type, cell_id))
                cell_id += 1
                current_cell = []
            
            current_type = "markdown"
            i += 1
            
            # Collect markdown content until closing triple quotes
            while i < len(lines):
                if lines[i].strip() == '"""':
                    break
                current_cell.append(lines[i])
                i += 1
            
            # Save markdown cell
            if current_cell:
                cells.append(create_cell(current_cell, current_type, cell_id))
                cell_id += 1
                current_cell = []
                current_type = None
            
        elif line.strip().startswith('"""') and line.strip().endswith('"""') and len(line.strip()) > 6:
            # Single line markdown
            if current_cell and current_type:
                cells.append(create_cell(current_cell, current_type, cell_id))
                cell_id += 1
                current_cell = []
            
            markdown_content = line.strip()[3:-3]
            if markdown_content:
                cells.append(create_cell([markdown_content], "markdown", cell_id))
                cell_id += 1
            current_type = None
            
        else:
            # Code content
            if current_type != "code":
                if current_cell and current_type:
                    cells.append(create_cell(current_cell, current_type, cell_id))
                    cell_id += 1
                    current_cell = []
                current_type = "code"
            
            if line.strip() or current_cell:  # Include line if it's not empty or we already have content
                current_cell.append(line)
        
        i += 1
    
    # Save final cell
    if current_cell and current_type:
        cells.append(create_cell(current_cell, current_type, cell_id))
    
    return cells

def create_cell(content, cell_type, cell_id):
    """Create a properly formatted notebook cell"""
    # Clean up content
    while content and not content[0].strip():
        content.pop(0)
    while content and not content[-1].strip():
        content.pop()
    
    if cell_type == "markdown":
        return {
            "cell_type": "markdown",
            "id": f"markdown-{cell_id}",
            "metadata": {},
            "source": content
        }
    else:
        return {
            "cell_type": "code",
            "execution_count": None,
            "id": f"code-{cell_id}",
            "metadata": {},
            "outputs": [],
            "source": content
        }

def create_notebook(cells):
    """Create a complete notebook structure"""
    return {
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

def convert_file(python_file, output_file):
    """Convert a single Python file to notebook"""
    print(f"Converting {python_file} -> {output_file}")
    
    cells = parse_python_notebook(python_file)
    notebook = create_notebook(cells)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    
    print(f"  Created {len(cells)} cells")
    return len(cells)

if __name__ == "__main__":
    conversions = [
        ("/Users/arunmenon/Downloads/module_01_notebook.py", "/Users/arunmenon/projects/AgentStarterKit/chapter_1/01_agent_foundations.ipynb"),
        ("/Users/arunmenon/Downloads/module_02_notebook.py", "/Users/arunmenon/projects/AgentStarterKit/chapter_2/02_memory_and_learning.ipynb"),
        ("/Users/arunmenon/Downloads/module_03_notebook.py", "/Users/arunmenon/projects/AgentStarterKit/chapter_3/03_tool_integration_and_environment.ipynb"),
        ("/Users/arunmenon/Downloads/module_04_notebook.py", "/Users/arunmenon/projects/AgentStarterKit/chapter_4/04_planning_and_goals.ipynb"),
    ]
    
    total_cells = 0
    for python_file, notebook_file in conversions:
        if Path(python_file).exists():
            cells = convert_file(python_file, notebook_file)
            total_cells += cells
        else:
            print(f"Warning: {python_file} not found")
    
    print(f"\nTotal cells created: {total_cells}")