#!/usr/bin/env python3
import json
import re

def fix_notebook(input_file, output_file):
    """Apply very specific fixes to the malformed notebook JSON"""
    print(f"Fixing {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix 1: The main issue - lines ending with )" followed by newlines and malformed closing
    # Pattern: module_progress_summary()" followed by newline and malformed structure
    
    # This specific pattern appears to be the core issue
    pattern = r'module_progress_summary\(\)"\s*\n\s*\]\s*\n\s*\}\\n",\s*\n\s*\],\\n",\s*\n\s*"metadata"'
    replacement = 'module_progress_summary()"\n   ]\n  }\n ],\n "metadata"'
    
    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)
        print("  Applied main pattern fix")
    
    # Fix 2: Remove other escaped characters in the metadata section
    content = re.sub(r'"metadata": \{\\n",', '"metadata": {', content)
    content = re.sub(r'\\n",\s*\n', '\n', content)
    
    # Fix 3: Clean up any remaining stray \\n", patterns
    content = re.sub(r'\\n",\s*$', '', content, flags=re.MULTILINE)
    
    # Fix 4: Fix unmatched quotes and braces
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        # Remove lines that are just escaped artifacts
        if line.strip() in ['\\n",', '\\",']:
            continue
        # Fix lines with just escaped newlines
        line = line.replace('\\n",', '')
        fixed_lines.append(line)
    
    content = '\n'.join(fixed_lines)
    
    # Try parsing
    try:
        notebook_data = json.loads(content)
        
        # Write the clean notebook
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(notebook_data, f, indent=1, ensure_ascii=False)
        
        print(f"  ✅ Success! {output_file} has {len(notebook_data.get('cells', []))} cells")
        return True
        
    except json.JSONDecodeError as e:
        print(f"  ❌ JSON error: {e}")
        
        # Show specific problem area
        lines = content.split('\n')
        if hasattr(e, 'lineno'):
            start = max(0, e.lineno - 2)
            end = min(len(lines), e.lineno + 2)
            print("  Problem area:")
            for i in range(start, end):
                marker = ">>>" if i == e.lineno - 1 else "   "
                print(f"  {marker} {i+1:3d}: {repr(lines[i])}")
        
        return False

# Let's also try a more surgical approach for the specific error patterns
def surgical_fix(input_file, output_file):
    """Surgical fix targeting the exact error locations"""
    print(f"Surgical fix for {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Based on the error messages, let's target specific line numbers
    fixes = [
        # For module_01: line 850 error
        (r'module_progress_summary\(\)"\s*\n\s*\]\s*\n\s*\}\\n",', 'module_progress_summary()"\n   ]\n  },'),
        
        # General fixes for the pattern we've seen
        (r'\],\\n",\s*\n\s*"metadata"', '],\n "metadata"'),
        (r'"metadata": \{\\n",', '"metadata": {'),
        (r'\\n",\s*\n', '\n'),
        (r'\\n",$', '"'),
        
        # Remove standalone escaped newline artifacts
        (r'^\s*\\n",\s*$', ''),
    ]
    
    original_content = content
    for pattern, replacement in fixes:
        old_content = content
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        if content != old_content:
            print(f"    Applied fix: {pattern[:30]}...")
    
    if content == original_content:
        print("    No fixes applied")
    
    try:
        notebook_data = json.loads(content)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(notebook_data, f, indent=1, ensure_ascii=False)
        
        print(f"  ✅ Surgical fix successful! {len(notebook_data.get('cells', []))} cells")
        return True
        
    except json.JSONDecodeError as e:
        print(f"  ❌ Surgical fix failed: {e}")
        return False

if __name__ == "__main__":
    files = [
        ("module_01_notebook.py", "chapter_1/01_agent_foundations.ipynb"),
        ("module_02_notebook.py", "chapter_2/02_memory_and_learning.ipynb"),
        ("module_03_notebook.py", "chapter_3/03_tool_integration_and_environment.ipynb"),
        ("module_04_notebook.py", "chapter_4/04_planning_and_goals.ipynb")
    ]
    
    print("Trying surgical fixes...")
    success = 0
    for input_file, output_file in files:
        print("\n" + "="*50)
        if surgical_fix(input_file, output_file):
            success += 1
    
    print(f"\n🎯 Surgical approach: {success}/{len(files)} files fixed")
    
    if success < len(files):
        print("\nTrying general fixes...")
        for input_file, output_file in files:
            print("\n" + "="*50)
            fix_notebook(input_file, output_file)