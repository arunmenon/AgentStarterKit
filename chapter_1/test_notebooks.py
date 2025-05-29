#!/usr/bin/env python3
"""Test all Module 1 notebooks"""

import subprocess
import os
import json

def test_notebook(notebook_path):
    """Test a single notebook by executing all cells"""
    print(f"\n📓 Testing: {notebook_path}")
    
    # Check if file exists and is valid JSON
    try:
        with open(notebook_path, 'r') as f:
            notebook = json.load(f)
        print("  ✅ Valid JSON structure")
        
        # Count cells
        code_cells = sum(1 for cell in notebook['cells'] if cell['cell_type'] == 'code')
        markdown_cells = sum(1 for cell in notebook['cells'] if cell['cell_type'] == 'markdown')
        print(f"  📊 {code_cells} code cells, {markdown_cells} markdown cells")
        
    except Exception as e:
        print(f"  ❌ JSON Error: {e}")
        return False
    
    # Execute notebook
    try:
        result = subprocess.run([
            'jupyter', 'nbconvert', 
            '--to', 'notebook', 
            '--execute',
            '--ExecutePreprocessor.timeout=60',
            '--output', notebook_path.replace('.ipynb', '_tested.ipynb'),
            notebook_path
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("  ✅ Execution successful")
            return True
        else:
            print(f"  ❌ Execution failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"  ❌ Execution error: {e}")
        return False

# Test all notebooks
notebooks = [
    "01_what_is_an_agent.ipynb",
    "02_react_pattern.ipynb", 
    "03_react_vs_rewoo.ipynb",
    "04_reflexion_pattern.ipynb",
    "05_advanced_prompting.ipynb",
    "06_reasoning_paradigms.ipynb",
    "07_evaluation_basics.ipynb"
]

print("🧪 Testing Module 1 Notebooks")
print("=" * 50)

# Check Ollama first
try:
    import requests
    response = requests.get("http://localhost:11434/api/tags", timeout=2)
    if response.status_code == 200:
        print("✅ Ollama is running")
    else:
        print("⚠️  Ollama not responding - agent notebooks may fail")
except:
    print("⚠️  Cannot connect to Ollama - agent notebooks may fail")

# Test each notebook
results = {}
for notebook in notebooks:
    if os.path.exists(notebook):
        results[notebook] = test_notebook(notebook)
    else:
        print(f"\n❌ Not found: {notebook}")
        results[notebook] = False

# Summary
print("\n" + "=" * 50)
print("📊 Test Summary:")
passed = sum(1 for r in results.values() if r)
print(f"✅ Passed: {passed}/{len(notebooks)}")
print(f"❌ Failed: {len(notebooks) - passed}/{len(notebooks)}")

if passed < len(notebooks):
    print("\n🔧 Failed notebooks:")
    for nb, result in results.items():
        if not result:
            print(f"  - {nb}")