#!/usr/bin/env python3
"""Manually fix the JSON error"""

# Read the file
with open('/Users/arunmenon/Desktop/notebooks/05_advanced_prompting.ipynb', 'r') as f:
    content = f.read()

# The issue is on line 868 where a string is not properly closed
# We need to find and fix this specific pattern

# Split into lines
lines = content.split('\n')

# Find and fix the problematic lines
fixed_lines = []
for i, line in enumerate(lines):
    line_num = i + 1
    
    # Line 868 is missing opening quote and has unescaped quotes
    if line_num == 868 and 'prompt += "\\nBehavioral guidelines:\\n"' in line:
        # This line should be a properly escaped JSON string
        fixed_lines.append('    "        prompt += \\"\\\\nBehavioral guidelines:\\\\n\\"\\n",')
    # Line 869 is missing quotes entirely  
    elif line_num == 869 and line.strip().startswith('for rule in persona.behavioral_rules:'):
        fixed_lines.append('    "        for rule in persona.behavioral_rules:\\n",')
    # Line 870 is also missing quotes
    elif line_num == 870 and 'prompt += f"•' in line:
        fixed_lines.append('    "            prompt += f\\"• {rule.capitalize()}\\\\n\\""')
    else:
        fixed_lines.append(line)

# Join and save
fixed_content = '\n'.join(fixed_lines)

with open('/Users/arunmenon/projects/AgentStarterKit/chapter_1/05_advanced_prompting_fixed2.ipynb', 'w') as f:
    f.write(fixed_content)

# Test validity
import json
try:
    with open('/Users/arunmenon/projects/AgentStarterKit/chapter_1/05_advanced_prompting_fixed2.ipynb', 'r') as f:
        notebook = json.load(f)
    print("✅ Successfully fixed the notebook!")
    
    # Save as the main file
    with open('/Users/arunmenon/projects/AgentStarterKit/chapter_1/05_advanced_prompting.ipynb', 'w') as f:
        json.dump(notebook, f, indent=1)
    print("✅ Saved as 05_advanced_prompting.ipynb")
    
except json.JSONDecodeError as e:
    print(f"❌ Error: {e}")
    # Show context around error
    error_line = e.lineno
    print(f"\nContext around line {error_line}:")
    for i in range(max(0, error_line-3), min(len(fixed_lines), error_line+2)):
        print(f"{i+1}: {fixed_lines[i]}")