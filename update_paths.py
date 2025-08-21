"""
Script to update file paths in project files after reorganization.
This script will update paths in Python, Markdown, and other text files.
"""

import os
import re
from pathlib import Path

def get_path_mappings():
    """Return a dictionary of old path to new path mappings."""
    return {
        # Old path patterns
        r'data/processed/cleaned_data/': 'data/processed/by_crime_type/',
        r'data/raw/': 'data/raw/ncrb_pdfs/',
        r'analysis/figures/': 'reports/figures/',
        r'src/data_': 'src/data/data_',
        # Add more mappings as needed
    }

def update_file_content(file_path, path_mappings):
    """Update paths in the given file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        updated = False
        for old_path, new_path in path_mappings.items():
            if re.search(old_path, content):
                content, count = re.subn(old_path, new_path, content)
                if count > 0:
                    updated = True
                    print(f"  - Updated {count} occurrence(s) of '{old_path}'")
        
        if updated:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        return False
    except Exception as e:
        print(f"  - Error processing {file_path}: {str(e)}")
        return False

def main():
    print("Starting path updates...")
    path_mappings = get_path_mappings()
    
    # File extensions to process
    extensions = ['.py', '.md', '.ipynb', '.json', '.yaml', '.yml']
    
    # Directories to process
    target_dirs = ['src', 'notebooks', 'docs', 'scripts']
    
    total_updated = 0
    
    for directory in target_dirs:
        if not os.path.exists(directory):
            print(f"Skipping non-existent directory: {directory}")
            continue
            
        print(f"\nProcessing directory: {directory}")
        
        for ext in extensions:
            for file_path in Path(directory).rglob(f'*{ext}'):
                if file_path.is_file() and not any(part.startswith('.') for part in file_path.parts):
                    print(f"\nChecking: {file_path}")
                    if update_file_content(file_path, path_mappings):
                        total_updated += 1
    
    print(f"\nUpdate complete! Modified {total_updated} files.")
    print("Please review the changes to ensure all paths were updated correctly.")

if __name__ == "__main__":
    main()
