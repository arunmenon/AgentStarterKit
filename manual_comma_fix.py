#!/usr/bin/env python3
import json

def manual_fix_file(input_file, output_file, error_line_num):
    """Manually fix the comma issue at a specific line"""
    print(f"Manually fixing {input_file} at line {error_line_num}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Total lines: {len(lines)}")
    print(f"Lines around error:")
    
    start = max(0, error_line_num - 5)
    end = min(len(lines), error_line_num + 5)
    
    for i in range(start, end):
        marker = ">>>" if i == error_line_num - 1 else "   "
        print(f"{marker} {i+1:4d}: {repr(lines[i])}")
    
    # The issue is typically a missing comma after a closing brace
    error_line = lines[error_line_num - 1]
    if error_line.strip() == '}':
        # Add a comma
        lines[error_line_num - 1] = error_line.rstrip() + ',\n'
        print(f"  Fixed: Added comma to line {error_line_num}")
        
        # Try to parse
        content = ''.join(lines)
        try:
            notebook_data = json.loads(content)
            
            # Write the fixed notebook
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(notebook_data, f, indent=1, ensure_ascii=False)
            
            print(f"  ✅ Successfully saved {output_file}")
            print(f"     Notebook has {len(notebook_data.get('cells', []))} cells")
            return True
            
        except json.JSONDecodeError as e:
            print(f"  ❌ Still has error after fix: {e}")
            return False
    else:
        print(f"  ❌ Line {error_line_num} doesn't match expected pattern")
        return False

# Fix each file with its known error line
files_to_fix = [
    ("module_01_notebook.py", "chapter_1/01_agent_foundations.ipynb", 850),
    ("module_02_notebook.py", "chapter_2/02_memory_and_learning.ipynb", 1453),
    ("module_03_notebook.py", "chapter_3/03_tool_integration_and_environment.ipynb", 1861),
    # Skip module 4 for now since it has a different error (unterminated string)
]

success_count = 0
for input_file, output_file, error_line in files_to_fix:
    print("\n" + "="*60)
    if manual_fix_file(input_file, output_file, error_line):
        success_count += 1

print(f"\n📊 Successfully fixed {success_count}/{len(files_to_fix)} files")