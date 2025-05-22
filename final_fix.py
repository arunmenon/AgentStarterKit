#!/usr/bin/env python3
import json
import re

def fix_notebook(input_file, output_file):
    """Fix the specific JSON formatting issues in the notebook files"""
    print(f"Fixing {input_file} -> {output_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # The main issue: lines like:  }\\n", should be just  },
    # These are at the end of cells where there are literal \n characters
    
    # Fix 1: Remove the \\n", pattern at end of cells
    content = re.sub(r'  }\\n",\s*$', '  },', content, flags=re.MULTILINE)
    
    # Fix 2: Remove similar patterns in the middle
    content = re.sub(r'  }\\n",\s*\n', '  },\n', content)
    
    # Fix 3: Fix the metadata section that has \\n", 
    content = re.sub(r' ],\\n",\s*\n "metadata"', ' ],\n "metadata"', content)
    content = re.sub(r' "metadata": {\\n",', ' "metadata": {', content)
    
    # Fix 4: Remove other stray \\n", patterns
    content = re.sub(r'\\n",\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'\\n",\s*\n', '\n', content)
    
    # Fix 5: Clean up any remaining literal \n in strings
    # Be careful to only fix obvious errors, not valid escaped newlines
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        # Skip lines that are properly formatted JSON strings
        if '"' in line and line.strip().endswith('",'):
            # This is likely a proper JSON string, don't modify
            fixed_lines.append(line)
        elif line.strip().endswith('\\n",'):
            # This is the problematic pattern - remove the \\n",
            fixed_line = line.replace('\\n",', '",')
            fixed_lines.append(fixed_line)
        else:
            fixed_lines.append(line)
    
    content = '\n'.join(fixed_lines)
    
    # Try to parse and validate
    try:
        notebook_data = json.loads(content)
        
        # Write the properly formatted notebook
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(notebook_data, f, indent=1, ensure_ascii=False)
        
        print(f"  ✅ Successfully fixed and saved {output_file}")
        print(f"     Notebook has {len(notebook_data.get('cells', []))} cells")
        return True
        
    except json.JSONDecodeError as e:
        print(f"  ❌ Still invalid JSON: {e}")
        
        # Show the problematic area
        lines = content.split('\n')
        if hasattr(e, 'lineno') and e.lineno <= len(lines):
            start = max(0, e.lineno - 3)
            end = min(len(lines), e.lineno + 3)
            print("     Context around error:")
            for i in range(start, end):
                marker = " --> " if i == e.lineno - 1 else "     "
                print(f"{marker}{i+1:4d}: {repr(lines[i])}")
        
        return False

if __name__ == "__main__":
    files = [
        ("module_01_notebook.py", "chapter_1/01_agent_foundations.ipynb"),
        ("module_02_notebook.py", "chapter_2/02_memory_and_learning.ipynb"), 
        ("module_03_notebook.py", "chapter_3/03_tool_integration_and_environment.ipynb"),
        ("module_04_notebook.py", "chapter_4/04_planning_and_goals.ipynb")
    ]
    
    success_count = 0
    for input_file, output_file in files:
        print("\n" + "="*60)
        if fix_notebook(input_file, output_file):
            success_count += 1
    
    print(f"\n📊 Fixed {success_count}/{len(files)} notebooks successfully!")