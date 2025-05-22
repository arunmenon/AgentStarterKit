#!/usr/bin/env python3
import json
import re
from pathlib import Path

def fix_json_syntax(file_path):
    """Fix common JSON syntax errors in notebook files"""
    print(f"Fixing {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Common fixes for JSON syntax errors
    fixes_applied = []
    
    # Fix 1: Missing commas after cell blocks
    # Look for pattern: }  followed by newline and ] without a comma
    pattern1 = r'(\}\s*\n\s*]\s*,\s*\n\s*"metadata")'
    if re.search(pattern1, content):
        content = re.sub(r'(\})\s*\n(\s*]\s*,\s*\n\s*"metadata")', r'\1,\n\2', content)
        fixes_applied.append("Added missing comma after cell block")
    
    # Fix 2: Missing commas between cells
    pattern2 = r'(\}\s*\n\s*\{\s*\n\s*"cell_type")'
    if re.search(pattern2, content):
        content = re.sub(r'(\})\s*\n(\s*\{\s*\n\s*"cell_type")', r'\1,\n\2', content)
        fixes_applied.append("Added missing commas between cells")
    
    # Fix 3: Check for unterminated strings (look for unescaped quotes in strings)
    # This is more complex and might need manual inspection
    
    # Try to parse and identify specific errors
    try:
        json.loads(content)
        print(f"  ✅ JSON is valid after fixes: {fixes_applied}")
        return content
    except json.JSONDecodeError as e:
        print(f"  ❌ JSON error at line {e.lineno}, col {e.colno}: {e.msg}")
        
        # Get the problematic line
        lines = content.split('\n')
        if e.lineno <= len(lines):
            error_line = lines[e.lineno - 1]
            print(f"     Problem line: {error_line}")
            
            # Try to fix specific issues
            if "Expecting ',' delimiter" in e.msg:
                # Find where comma is missing
                if e.colno < len(error_line):
                    char_at_error = error_line[e.colno - 1] if e.colno > 0 else ''
                    print(f"     Character at error: '{char_at_error}'")
                    
                    # If it's a closing brace that needs a comma
                    if char_at_error == '}' and e.colno < len(error_line):
                        # Add comma after the brace
                        new_line = error_line[:e.colno] + ',' + error_line[e.colno:]
                        lines[e.lineno - 1] = new_line
                        content = '\n'.join(lines)
                        fixes_applied.append(f"Added comma at line {e.lineno}, col {e.colno}")
                        
                        # Try parsing again
                        try:
                            json.loads(content)
                            print(f"  ✅ Fixed after adding comma: {fixes_applied}")
                            return content
                        except json.JSONDecodeError as e2:
                            print(f"  ❌ Still invalid after comma fix: {e2.msg}")
            
            elif "Unterminated string" in e.msg:
                print(f"     Need to fix unterminated string at line {e.lineno}")
                # This requires more careful analysis
        
        print(f"  ❌ Could not automatically fix JSON errors")
        return None

def process_file(input_file, output_file):
    """Process a single file"""
    fixed_content = fix_json_syntax(input_file)
    if fixed_content:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print(f"  ✅ Saved fixed version to {output_file}")
        return True
    return False

if __name__ == "__main__":
    files_to_fix = [
        ("module_01_notebook.py", "chapter_1/01_agent_foundations.ipynb"),
        ("module_02_notebook.py", "chapter_2/02_memory_and_learning.ipynb"),
        ("module_03_notebook.py", "chapter_3/03_tool_integration_and_environment.ipynb"),
        ("module_04_notebook.py", "chapter_4/04_planning_and_goals.ipynb"),
    ]
    
    for input_file, output_file in files_to_fix:
        if Path(input_file).exists():
            print(f"\n{'='*60}")
            success = process_file(input_file, output_file)
            if not success:
                print(f"Failed to fix {input_file}")
        else:
            print(f"File not found: {input_file}")