#!/usr/bin/env python3
import json
import re

def convert_string_representation_to_json(input_file, output_file):
    """Convert Python string representation back to proper JSON"""
    print(f"Converting {input_file} to proper JSON")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # The files appear to be Python string representations of JSON
    # Key patterns to fix:
    # 1. }\\n", should become },
    # 2. ],\\n", should become ],  
    # 3. \\"metadata\\": {\\n", should become "metadata": {
    # 4. Other escaped characters
    
    print("  Applying fixes...")
    fixes_applied = []
    
    # Fix 1: End of cells pattern }\\n",
    original = content
    content = re.sub(r'  }\\n",\s*\n', '  },\n', content)
    if content != original:
        fixes_applied.append("Fixed cell endings")
        original = content
    
    # Fix 2: End of cells array ],\\n",
    content = re.sub(r' ],\\n",\s*\n', ' ],\n', content)
    if content != original:
        fixes_applied.append("Fixed cells array endings")
        original = content
    
    # Fix 3: Metadata section  \\"metadata\\": {\\n",
    content = re.sub(r' \\"metadata\\": \{\\n",\s*\n', ' "metadata": {\n', content)
    if content != original:
        fixes_applied.append("Fixed metadata section")
        original = content
    
    # Fix 4: Other escaped quotes in keys
    content = re.sub(r'\\"([^"]+)\\":', r'"\1":', content)
    if content != original:
        fixes_applied.append("Fixed escaped quotes in keys")
        original = content
    
    # Fix 5: Remove remaining \\n", artifacts
    content = re.sub(r'\\n",\s*\n', '\n', content)
    if content != original:
        fixes_applied.append("Removed newline artifacts")
        original = content
    
    # Fix 6: Clean up any remaining escape patterns at end of file
    content = re.sub(r'\\n",\s*\n\s*}\s*$', '\n  }\n }', content, flags=re.MULTILINE)
    
    print(f"    Applied fixes: {fixes_applied}")
    
    try:
        # Try to parse the JSON
        notebook_data = json.loads(content)
        
        # Write the properly formatted notebook
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(notebook_data, f, indent=1, ensure_ascii=False)
        
        print(f"  ✅ Success! Created {output_file} with {len(notebook_data.get('cells', []))} cells")
        return True
        
    except json.JSONDecodeError as e:
        print(f"  ❌ JSON error after fixes: {e}")
        
        # Save debug version
        debug_file = output_file.replace('.ipynb', '_debug.json')
        with open(debug_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"    Saved debug version to {debug_file}")
        
        # Show error context
        lines = content.split('\n')
        if hasattr(e, 'lineno') and e.lineno <= len(lines):
            start = max(0, e.lineno - 3)
            end = min(len(lines), e.lineno + 3)
            print("    Error context:")
            for i in range(start, end):
                marker = ">>>" if i == e.lineno - 1 else "   "
                print(f"    {marker} {i+1:4d}: {repr(lines[i])}")
        
        return False

def process_all_files():
    """Process all module files"""
    files = [
        ("module_01_notebook.py", "chapter_1/01_agent_foundations.ipynb"),
        ("module_02_notebook.py", "chapter_2/02_memory_and_learning.ipynb"),
        ("module_03_notebook.py", "chapter_3/03_tool_integration_and_environment.ipynb"),
        ("module_04_notebook.py", "chapter_4/04_planning_and_goals.ipynb")
    ]
    
    success_count = 0
    for input_file, output_file in files:
        print("\n" + "="*60)
        if convert_string_representation_to_json(input_file, output_file):
            success_count += 1
    
    print(f"\n📊 Successfully converted {success_count}/{len(files)} files")
    return success_count == len(files)

if __name__ == "__main__":
    process_all_files()