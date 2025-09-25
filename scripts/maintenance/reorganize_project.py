import os
import shutil
from pathlib import Path

def create_directory(path):
    """Create directory if it doesn't exist"""
    path.mkdir(parents=True, exist_ok=True)
    return path

def move_file(src, dest):
    """Move file from src to dest, creating parent directories if needed"""
    if src.exists() and src.is_file():
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dest))
        print(f"Moved: {src} -> {dest}")

# Define project root
PROJECT_ROOT = Path(__file__).parent

# Define new directory structure
DIR_STRUCTURE = {
    'app': {
        'config': {},
        'models': {},
        'routes': {
            'api': {
                'v1': {
                    'endpoints': {}
                }
            }
        },
        'static': {
            'css': {},
            'js': {},
            'images': {}
        },
        'templates': {
            'auth': {},
            'main': {}
        },
        'utils': {}
    },
    'data': {
        'raw': {},
        'processed': {},
        'external': {}
    },
    'tests': {
        'unit': {},
        'integration': {}
    },
    'docs': {
        'api': {},
        'deployment': {},
        'development': {}
    },
    'scripts': {
        'data_processing': {},
        'deployment': {}
    }
}

def create_structure(base_path, structure):
    """Create directory structure recursively"""
    for name, children in structure.items():
        current_path = base_path / name
        create_directory(current_path)
        if children:
            create_structure(current_path, children)

def move_existing_files():
    """Move existing files to their new locations"""
    # Move configuration files
    if (PROJECT_ROOT / 'config').exists():
        for config_file in (PROJECT_ROOT / 'config').glob('*'):
            if config_file.is_file():
                move_file(
                    config_file,
                    PROJECT_ROOT / 'app' / 'config' / config_file.name
                )
    
    # Move data files
    if (PROJECT_ROOT / 'crime data').exists():
        for data_file in (PROJECT_ROOT / 'crime data').glob('*'):
            if data_file.is_file():
                move_file(
                    data_file,
                    PROJECT_ROOT / 'data' / 'raw' / data_file.name
                )
    
    # Move map files
    if (PROJECT_ROOT / 'Maps').exists():
        move_file(
            PROJECT_ROOT / 'Maps',
            PROJECT_ROOT / 'app' / 'static' / 'maps'
        )
    
    # Move documentation
    if (PROJECT_ROOT / 'docs').exists():
        for doc_file in (PROJECT_ROOT / 'docs').glob('*'):
            if doc_file.is_file() and doc_file.suffix in ['.md', '.html']:
                move_file(
                    doc_file,
                    PROJECT_ROOT / 'docs' / 'development' / doc_file.name
                )

def main():
    print("🚀 Reorganizing project structure...")
    
    # Create new directory structure
    create_structure(PROJECT_ROOT, DIR_STRUCTURE)
    
    # Move existing files to new locations
    move_existing_files()
    
    # Create empty __init__.py files in Python packages
    for root, dirs, _ in os.walk(PROJECT_ROOT / 'app'):
        for dir_name in dirs:
            init_file = Path(root) / dir_name / '__init__.py'
            if not init_file.exists():
                init_file.touch()
    
    print("✅ Project reorganization complete!")
    print("\nNext steps:")
    print("1. Review the new directory structure")
    print("2. Update import statements in your Python files")
    print("3. Update configuration files with new paths")
    print("4. Run tests to ensure everything works")

if __name__ == "__main__":
    main()