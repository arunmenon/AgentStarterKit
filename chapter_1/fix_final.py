#!/usr/bin/env python3
"""Final fix for the notebook JSON issues"""

import json

# Read the original file
with open('/Users/arunmenon/Desktop/notebooks/05_advanced_prompting.ipynb', 'r') as f:
    lines = f.readlines()

# Fix the specific problematic lines
for i in range(len(lines)):
    line_num = i + 1
    
    # Line 868: Missing comma at the end
    if line_num == 868:
        if lines[i].strip().endswith('"'):
            lines[i] = lines[i].rstrip() + ',\n'
            print(f"Fixed line {line_num}: Added missing comma")
    
    # Lines 869-871: Missing quotes and proper JSON formatting
    elif line_num == 869:
        if not lines[i].strip().startswith('"'):
            lines[i] = '    "        for rule in persona.behavioral_rules:\\n",\n'
            print(f"Fixed line {line_num}: Added quotes")
    
    elif line_num == 870:
        if not lines[i].strip().startswith('"'):
            lines[i] = '    "            prompt += f\\"• {rule.capitalize()}\\\\n\\"\\n",\n'
            print(f"Fixed line {line_num}: Added quotes")
    
    elif line_num == 871:
        if lines[i].strip() == '':
            lines[i] = '    "        \\n",\n'
            print(f"Fixed line {line_num}: Added quotes to empty line")
    
    elif line_num == 872:
        if not lines[i].strip().startswith('"'):
            lines[i] = '    "        prompt += f\\"\\\\nCommunication style:\\\\n• {persona.communication_style.capitalize()}\\\\n\\"\\n",\n'
            print(f"Fixed line {line_num}: Added quotes")

# Write the fixed content
fixed_path = '/Users/arunmenon/projects/AgentStarterKit/chapter_1/05_advanced_prompting.ipynb'
with open(fixed_path, 'w') as f:
    f.writelines(lines)

# Validate the fixed file
try:
    with open(fixed_path, 'r') as f:
        notebook = json.load(f)
    print(f"\n✅ Successfully fixed! The notebook now has {len(notebook['cells'])} cells")
    print("✅ Saved as 05_advanced_prompting.ipynb")
except json.JSONDecodeError as e:
    print(f"\n❌ Still has error at line {e.lineno}: {e.msg}")
    # Show the problematic line
    if e.lineno <= len(lines):
        print(f"Line {e.lineno}: {repr(lines[e.lineno-1])}")