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
            # This might be a direct notebook file that just has JSON syntax errors
            print(f"ℹ️ Notebook appears to be direct format, checking for syntax errors...")
            
            # Check if it's a valid notebook already
            if 'cells' in malformed_nb and 'metadata' in malformed_nb:
                print(f"✅ Notebook is already properly formatted with {len(malformed_nb['cells'])} cells")
                return True
            else:
                print(f"❌ Notebook has unexpected structure")
                return False
            
    except json.JSONDecodeError as e:
        # The file has JSON syntax errors, let's try to fix them
        print(f"⚠️ JSON syntax error: {e}")
        return fix_json_syntax_errors(notebook_path)
    except Exception as e:
        print(f"❌ Error processing notebook: {e}")
        return False

def fix_json_syntax_errors(notebook_path):
    """Fix common JSON syntax errors"""
    print(f"  Attempting to fix JSON syntax errors in {notebook_path}")
    
    try:
        # Read as text
        with open(notebook_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Make a backup
        backup_path = notebook_path.with_suffix('.broken.backup')
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Try some common fixes
        fixes_applied = []
        
        # Fix 1: Missing commas after cells
        import re
        original_content = content
        
        # Look for cell ending patterns that are missing commas
        content = re.sub(r'(\})\s*\n\s*(\{[^}]*"cell_type")', r'\1,\n  \2', content)
        if content != original_content:
            fixes_applied.append("Added missing commas between cells")
            original_content = content
        
        # Fix 2: Missing commas at end of cell arrays  
        content = re.sub(r'(\})\s*\n\s*(\])', r'\1\n \2', content)
        if content != original_content:
            fixes_applied.append("Fixed cell array endings")
        
        # Try to parse again
        try:
            notebook_data = json.loads(content)
            
            # Write the fixed version
            with open(notebook_path, 'w', encoding='utf-8') as f:
                json.dump(notebook_data, f, indent=1)
            
            print(f"  ✅ Fixed JSON syntax! Applied: {fixes_applied}")
            print(f"     Backup saved to: {backup_path}")
            return True
            
        except json.JSONDecodeError as e2:
            print(f"  ❌ Could not fix JSON syntax: {e2}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error during JSON fix: {e}")
        return False

def fix_all_notebooks(directory):
    """
    Fix all notebooks in a directory recursively
    """
    directory = Path(directory)
    fixed_count = 0
    
    # Find all .py files that should be notebooks
    notebook_files = [
        directory / "module_01_notebook.py",
        directory / "module_02_notebook.py", 
        directory / "module_03_notebook.py",
        directory / "module_04_notebook.py"
    ]
    
    # Convert them to .ipynb paths
    target_files = [
        directory / "chapter_1" / "01_agent_foundations.ipynb",
        directory / "chapter_2" / "02_memory_and_learning.ipynb",
        directory / "chapter_3" / "03_tool_integration_and_environment.ipynb", 
        directory / "chapter_4" / "04_planning_and_goals.ipynb"
    ]
    
    print(f"Found {len(notebook_files)} source files to convert")
    print("=" * 60)
    
    for src_file, tgt_file in zip(notebook_files, target_files):
        if src_file.exists():
            # Copy source to target first
            import shutil
            shutil.copy2(src_file, tgt_file)
            print(f"Copied {src_file} -> {tgt_file}")
            
            # Now try to fix it
            if fix_malformed_notebook(tgt_file):
                fixed_count += 1
            print("-" * 60)
        else:
            print(f"Source file not found: {src_file}")
    
    print(f"\n📊 Summary:")
    print(f"   Total notebooks: {len(notebook_files)}")
    print(f"   Fixed: {fixed_count}")
    print(f"   Failed: {len(notebook_files) - fixed_count}")

# Usage
if __name__ == "__main__":
    fix_all_notebooks(".")