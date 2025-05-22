#!/usr/bin/env python3
import json
import re
from pathlib import Path

def fix_literal_newlines(file_path):
    """Fix literal \\n characters in JSON strings"""
    print(f"Fixing literal newlines in {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix literal \n characters in JSON strings
    # This is a very specific fix for the malformed JSON
    fixes_applied = []
    
    # Replace literal \n with actual newlines in source arrays
    # Pattern: "text\\n" should become "text\n"
    original_len = len(content)
    content = content.replace('\\n",', '\n",')
    content = content.replace('\\n"', '\n"')
    
    if len(content) != original_len:
        fixes_applied.append("Fixed literal \\n characters")
    
    # Fix missing commas at end of cells
    # Look for }  followed by ] (end of cell, end of cells array)
    content = re.sub(r'(\})\s*\n\s*(\]\s*,\s*\n\s*"metadata")', r'\1,\n  \2', content)
    
    # Fix unterminated strings by finding unmatched quotes
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        if '"' in line and line.strip().startswith('"') and not line.strip().endswith('",') and not line.strip().endswith('"'):
            # This might be an unterminated string, add closing quote and comma
            if not line.rstrip().endswith('"'):
                line = line.rstrip() + '",'
                fixes_applied.append(f"Fixed unterminated string at line {i+1}")
        fixed_lines.append(line)
    
    content = '\n'.join(fixed_lines)
    
    # Try to parse the JSON
    try:
        parsed = json.loads(content)
        print(f"  ✅ JSON is now valid! Fixes applied: {fixes_applied}")
        return content
    except json.JSONDecodeError as e:
        print(f"  ❌ Still invalid JSON: {e.msg} at line {e.lineno}")
        
        # Try one more specific fix for the exact error patterns we're seeing
        if "Expecting ',' delimiter" in e.msg:
            lines = content.split('\n')
            error_line_idx = e.lineno - 1
            
            if error_line_idx < len(lines):
                error_line = lines[error_line_idx]
                print(f"     Error line: {repr(error_line)}")
                
                # If line ends with }\n", it should end with },\n"
                if error_line.strip() == '}':
                    lines[error_line_idx] = error_line.replace('}', '},')
                    content = '\n'.join(lines)
                    fixes_applied.append(f"Added comma after brace at line {e.lineno}")
                    
                    try:
                        json.loads(content)
                        print(f"  ✅ Fixed with comma addition! Fixes: {fixes_applied}")
                        return content
                    except json.JSONDecodeError as e2:
                        print(f"  ❌ Still invalid: {e2.msg}")
        
        return None

def process_notebook_file(input_file, output_file):
    """Process and fix a notebook file"""
    fixed_content = fix_literal_newlines(input_file)
    if fixed_content:
        # Write the fixed content
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print(f"  ✅ Saved to {output_file}")
        
        # Verify it's valid
        try:
            with open(output_file, 'r') as f:
                json.load(f)
            print(f"  ✅ Verified: {output_file} is valid JSON")
            return True
        except json.JSONDecodeError as e:
            print(f"  ❌ Verification failed: {e.msg}")
            return False
    return False

if __name__ == "__main__":
    files_to_fix = [
        ("module_01_notebook.py", "chapter_1/01_agent_foundations.ipynb"),
        ("module_02_notebook.py", "chapter_2/02_memory_and_learning.ipynb"),
        ("module_03_notebook.py", "chapter_3/03_tool_integration_and_environment.ipynb"),
        ("module_04_notebook.py", "chapter_4/04_planning_and_goals.ipynb"),
    ]
    
    success_count = 0
    for input_file, output_file in files_to_fix:
        if Path(input_file).exists():
            print(f"\n{'='*80}")
            if process_notebook_file(input_file, output_file):
                success_count += 1
        else:
            print(f"File not found: {input_file}")
    
    print(f"\n📊 Successfully fixed {success_count}/{len(files_to_fix)} files")