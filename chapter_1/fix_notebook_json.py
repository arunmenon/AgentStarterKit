#!/usr/bin/env python3
"""Fix JSON issues in notebook"""

import json
import re

# Read the problematic notebook
with open('05_advanced_prompting.ipynb', 'r') as f:
    content = f.read()

# Common issues in notebooks:
# 1. Unescaped quotes in strings
# 2. Missing commas between list items

# Try to parse and fix
try:
    # First attempt - direct parse
    notebook = json.loads(content)
    print("✅ Notebook is already valid JSON")
except json.JSONDecodeError as e:
    print(f"Found JSON error at position {e.pos}: {e.msg}")
    
    # Try to fix common issues
    # Look for patterns like: "string" without comma after
    lines = content.split('\n')
    
    # Check line 868 area
    for i in range(865, 870):
        if i < len(lines):
            line = lines[i]
            # Look for missing escape before quotes
            if '"\\n"' in line and not line.strip().endswith(','):
                lines[i] = line.rstrip() + ','
                print(f"Fixed line {i+1}: Added missing comma")
    
    # Write fixed content
    fixed_content = '\n'.join(lines)
    
    # Try to parse again
    try:
        notebook = json.loads(fixed_content)
        with open('05_advanced_prompting_fixed.ipynb', 'w') as f:
            json.dump(notebook, f, indent=2)
        print("✅ Fixed and saved as 05_advanced_prompting_fixed.ipynb")
    except json.JSONDecodeError as e2:
        print(f"Still has error: {e2}")
        print("Manual fix needed")