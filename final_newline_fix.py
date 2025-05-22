#!/usr/bin/env python3
import json
import re

def fix_literal_newlines_in_json_strings(input_file, output_file):
    """Fix literal newlines within JSON string values"""
    print(f"Fixing literal newlines in {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this line starts a JSON string but doesn't end it properly
        # (indicating it has embedded literal newlines)
        if (line.strip().startswith('"') and 
            not line.rstrip().endswith('",') and 
            not line.rstrip().endswith('"')):
            
            # This string spans multiple lines - collect all lines for this string
            string_parts = [line.rstrip('\n')]
            j = i + 1
            
            # Keep collecting until we find a line that ends the string
            while j < len(lines):
                next_line = lines[j]
                string_parts.append(next_line.rstrip('\n'))
                
                # Check if this line ends the string
                if (next_line.rstrip().endswith('",') or 
                    next_line.rstrip().endswith('"')):
                    break
                j += 1
            
            # Now combine all parts into a single line with proper \\n escapes
            if len(string_parts) > 1:
                # Join with \\n instead of literal newlines
                combined = string_parts[0]
                for part in string_parts[1:]:
                    # Remove leading whitespace from continuation lines since they're not meaningful
                    part = part.lstrip()
                    combined += '\\n' + part
                
                fixed_lines.append(combined + '\n')
                i = j + 1  # Skip all the lines we just processed
            else:
                fixed_lines.append(line)
                i += 1
        else:
            fixed_lines.append(line)
            i += 1
    
    # Join all lines and try to parse
    content = ''.join(fixed_lines)
    
    # Additional cleanup for known patterns
    # Fix the specific end-of-file issues we've seen
    content = re.sub(r'module_progress_summary\(\)"\s*\n\s*\]\s*\n\s*\}\\n",\s*\n\s*\],\\n",\s*\n\s*"metadata"', 
                     'module_progress_summary()"\n   ]\n  }\n ],\n "metadata"', content)
    
    # Clean up escaped artifacts
    content = re.sub(r'"metadata": \{\\n",', '"metadata": {', content)
    content = re.sub(r'\\n",\s*\n\s*\}', '"\n  }', content)
    content = re.sub(r'\\n",\s*\n', '\n', content)
    
    try:
        notebook_data = json.loads(content)
        
        # Success! Write the proper notebook
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(notebook_data, f, indent=1, ensure_ascii=False)
        
        print(f"  ✅ Successfully fixed! Created notebook with {len(notebook_data.get('cells', []))} cells")
        return True
        
    except json.JSONDecodeError as e:
        print(f"  ❌ Still has JSON errors: {e}")
        
        # Save the intermediate result for debugging
        debug_file = output_file.replace('.ipynb', '_debug.json')
        with open(debug_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"     Saved debug version to {debug_file}")
        
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
        if fix_literal_newlines_in_json_strings(input_file, output_file):
            success_count += 1
    
    print(f"\n📊 Successfully fixed {success_count}/{len(files)} notebooks!")