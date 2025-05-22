#!/usr/bin/env python3
import json
import os
from pathlib import Path

def fix_malformed_notebook(notebook_path):
    """
    Fix notebooks where the entire content is wrapped in a code cell
    """
    print(f"Processing: {notebook_path}")
    
    try:
        # Read the malformed notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the outer JSON structure
        malformed_nb = json.loads(content)
        
        # Check if this is a malformed notebook
        if (len(malformed_nb.get('cells', [])) > 0 and 
            malformed_nb['cells'][0].get('cell_type') == 'code'):
            
            # Get the source content from the first cell
            source = malformed_nb['cells'][0].get('source', [])
            
            # Join the source lines to create the full JSON string
            if isinstance(source, list):
                json_string = ''.join(source)
            else:
                json_string = source
            
            # The content should be a JSON string - let's parse it
            try:
                # This is the actual notebook that was incorrectly wrapped
                actual_notebook = json.loads(json_string)
                
                # Validate it has the expected notebook structure
                if ('cells' in actual_notebook and 
                    'metadata' in actual_notebook and
                    isinstance(actual_notebook['cells'], list)):
                    
                    # Backup the original
                    backup_path = notebook_path.with_suffix('.backup.json')
                    with open(backup_path, 'w', encoding='utf-8') as f:
                        json.dump(malformed_nb, f, indent=1)
                    
                    # Save the properly structured notebook
                    with open(notebook_path, 'w', encoding='utf-8') as f:
                        json.dump(actual_notebook, f, indent=1)
                    
                    print(f"✅ Fixed: {notebook_path}")
                    print(f"   Backup saved to: {backup_path}")
                    print(f"   Cells in fixed notebook: {len(actual_notebook['cells'])}")
                    return True
                else:
                    print(f"❌ Invalid notebook structure in nested content")
                    return False
                    
            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse nested JSON: {e}")
                print(f"   First 200 chars of content: {json_string[:200]}")
                return False
        else:
            print(f"ℹ️ Notebook appears to be correctly formatted")
            return False
            
    except Exception as e:
        print(f"❌ Error processing notebook: {e}")
        return False

def fix_all_notebooks(directory):
    """
    Fix all notebooks in a directory recursively
    """
    directory = Path(directory)
    fixed_count = 0
    
    # Find all .ipynb files
    notebook_files = list(directory.rglob("*.ipynb"))
    
    if not notebook_files:
        print("No notebook files found!")
        return
    
    print(f"Found {len(notebook_files)} notebook files")
    print("=" * 60)
    
    for notebook_path in notebook_files:
        if fix_malformed_notebook(notebook_path):
            fixed_count += 1
        print("-" * 60)
    
    print(f"\n📊 Summary:")
    print(f"   Total notebooks: {len(notebook_files)}")
    print(f"   Fixed: {fixed_count}")
    print(f"   Unchanged: {len(notebook_files) - fixed_count}")

if __name__ == "__main__":
    fix_all_notebooks(".")