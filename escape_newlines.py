#!/usr/bin/env python3
import json
import re

def fix_newlines_in_json(input_file, output_file):
    """Fix literal newlines in JSON strings"""
    print(f"Processing {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    in_source_array = False
    brace_count = 0
    
    for i, line in enumerate(lines):
        # Track if we're inside a "source" array
        if '"source": [' in line:
            in_source_array = True
        
        # Track braces to know when we exit arrays/objects
        brace_count += line.count('[') - line.count(']')
        
        if in_source_array and brace_count <= 0:
            in_source_array = False
        
        # If we're in a source array and this line doesn't end with ", or ],
        # it likely has an embedded newline that should be escaped
        if in_source_array and line.strip().startswith('"') and not (line.strip().endswith('",') or line.strip().endswith('"')):
            # This line has an embedded newline, need to join with next line
            current_line = line.rstrip('\n')
            
            # Keep collecting lines until we find the end of this string
            j = i + 1
            while j < len(lines) and not lines[j].strip().endswith('",') and not lines[j].strip().endswith('"'):
                current_line += '\\n' + lines[j].rstrip('\n')
                j += 1
            
            # Add the final line
            if j < len(lines):
                current_line += '\\n' + lines[j].rstrip('\n')
            
            # Add this fixed line and skip the lines we've processed
            fixed_lines.append(current_line + '\n')
            
            # Skip ahead
            for _ in range(j - i):
                if i + 1 < len(lines):
                    i += 1
        else:
            fixed_lines.append(line)
    
    # Join and try to parse
    content = ''.join(fixed_lines)
    
    try:
        # Parse to validate
        notebook_data = json.loads(content)
        
        # Write the clean version
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(notebook_data, f, indent=1, ensure_ascii=False)
        
        print(f"  ✅ Successfully processed {output_file}")
        print(f"     Created notebook with {len(notebook_data.get('cells', []))} cells")
        return True
        
    except json.JSONDecodeError as e:
        print(f"  ❌ JSON parsing failed: {e}")
        return False

def simple_line_by_line_fix(input_file, output_file):
    """Simple approach: read line by line and fix obvious issues"""
    print(f"Simple fix for {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into lines but preserve the structure
    lines = content.split('\n')
    fixed_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # If this line starts with whitespace and a quote but doesn't end properly,
        # it probably has embedded newlines
        if (line.strip().startswith('"') and 
            not line.strip().endswith('",') and 
            not line.strip().endswith('"') and
            '"source":' in ''.join(lines[max(0, i-5):i])):  # Check if we're in a source array
            
            # Collect all lines until we find the end of this string
            full_string = line.rstrip()
            j = i + 1
            
            while j < len(lines):
                next_line = lines[j].rstrip()
                if next_line.strip().endswith('",') or next_line.strip().endswith('"'):
                    # Found the end
                    full_string += '\\n' + next_line
                    break
                else:
                    # Continue building the string
                    full_string += '\\n' + next_line
                j += 1
            
            fixed_lines.append(full_string)
            i = j + 1  # Skip all the lines we processed
        else:
            fixed_lines.append(line)
            i += 1
    
    # Rejoin content
    fixed_content = '\n'.join(fixed_lines)
    
    try:
        notebook_data = json.loads(fixed_content)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(notebook_data, f, indent=1, ensure_ascii=False)
        
        print(f"  ✅ Simple fix successful for {output_file}")
        print(f"     Cells: {len(notebook_data.get('cells', []))}")
        return True
        
    except json.JSONDecodeError as e:
        print(f"  ❌ Simple fix failed: {e}")
        return False

if __name__ == "__main__":
    files = [
        ("module_01_notebook.py", "chapter_1/01_agent_foundations.ipynb"),
        ("module_02_notebook.py", "chapter_2/02_memory_and_learning.ipynb"),
        ("module_03_notebook.py", "chapter_3/03_tool_integration_and_environment.ipynb"),
        ("module_04_notebook.py", "chapter_4/04_planning_and_goals.ipynb")
    ]
    
    for input_file, output_file in files:
        print("\n" + "="*60)
        success = simple_line_by_line_fix(input_file, output_file)