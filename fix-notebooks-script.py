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
            malformed_nb = json.load(f)
        
        # Check if this is a malformed notebook
        if (len(malformed_nb.get('cells', [])) > 0 and 
            malformed_nb['cells'][0].get('cell_type') == 'code' and
            malformed_nb['cells'][0].get('source', [])):
            
            # Get the source content
            source = malformed_nb['cells'][0]['source']
            
            # Join the source if it's a list
            if isinstance(source, list):
                source = ''.join(source)
            
            # Check if the source contains a nested notebook structure
            if source.strip().startswith('{') and '"cells":' in source:
                try:
                    # Parse the nested notebook from the string
                    # Remove escape characters
                    fixed_source = source.replace('\\"', '"').replace('\\n', '\n').replace('\\\\', '\\')
                    
                    # Find the actual JSON content
                    json_start = fixed_source.find('{')
                    json_end = fixed_source.rfind('}') + 1
                    
                    if json_start >= 0 and json_end > json_start:
                        json_content = fixed_source[json_start:json_end]
                        
                        # Parse the actual notebook
                        actual_notebook = json.loads(json_content)
                        
                        # Validate it has the expected structure
                        if 'cells' in actual_notebook and 'metadata' in actual_notebook:
                            # Backup the original
                            backup_path = notebook_path.with_suffix('.backup.json')
                            with open(backup_path, 'w', encoding='utf-8') as f:
                                json.dump(malformed_nb, f, indent=1)
                            
                            # Save the fixed notebook
                            with open(notebook_path, 'w', encoding='utf-8') as f:
                                json.dump(actual_notebook, f, indent=1)
                            
                            print(f"✅ Fixed: {notebook_path}")
                            print(f"   Backup saved to: {backup_path}")
                            return True
                        else:
                            print(f"❌ Invalid notebook structure in nested content")
                            return False
                            
                except json.JSONDecodeError as e:
                    print(f"❌ Failed to parse nested JSON: {e}")
                    return False
            else:
                print(f"ℹ️ Not a malformed notebook (no nested structure found)")
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

# Usage
if __name__ == "__main__":
    # Run this script in the root of your AgentStarterKit repository
    fix_all_notebooks(".")
    
    # Or specify the exact path
    # fix_all_notebooks("/path/to/AgentStarterKit")