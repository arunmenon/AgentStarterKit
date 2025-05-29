#!/usr/bin/env python3
"""Fix the JSON error in notebook 05"""

# Read the file as text
with open('/Users/arunmenon/Desktop/notebooks/05_advanced_prompting.ipynb', 'r') as f:
    lines = f.readlines()

# Fix line 868 (index 867) - the line with unescaped quotes
# Original: prompt += "\\nBehavioral guidelines:\\n"
# Fixed: prompt += \"\\nBehavioral guidelines:\\n\"

for i in range(len(lines)):
    # Around line 868
    if i >= 865 and i <= 870:
        # Check for the problematic pattern
        if 'prompt += "\\nBehavioral guidelines:\\n"' in lines[i]:
            # This line needs to be inside a JSON string, so escape the quotes
            lines[i] = '    "        prompt += \\"\\\\nBehavioral guidelines:\\\\n\\"\\n",\n'
            print(f"Fixed line {i+1}")
        # Also check the next line that might be missing quotes
        elif 'for rule in persona.behavioral_rules:' in lines[i] and not lines[i].strip().startswith('"'):
            lines[i] = '    "        for rule in persona.behavioral_rules:\\n",\n'
            print(f"Fixed line {i+1}")
        elif 'prompt += f"•' in lines[i] and not lines[i].strip().startswith('"'):
            lines[i] = '    "            prompt += f\\"• {rule.capitalize()}\\\\n\\"\\n"\n'
            print(f"Fixed line {i+1}")

# Write the fixed content
with open('/Users/arunmenon/projects/AgentStarterKit/chapter_1/05_advanced_prompting_fixed.ipynb', 'w') as f:
    f.writelines(lines)

print("Wrote fixed file to 05_advanced_prompting_fixed.ipynb")

# Test if it's valid JSON now
import json
try:
    with open('/Users/arunmenon/projects/AgentStarterKit/chapter_1/05_advanced_prompting_fixed.ipynb', 'r') as f:
        json.load(f)
    print("✅ Fixed file is valid JSON!")
except json.JSONDecodeError as e:
    print(f"❌ Still has error: {e}")
    print(f"Error at line {e.lineno}")