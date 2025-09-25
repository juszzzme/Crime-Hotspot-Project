#!/usr/bin/env python3
"""
Script to reorganize project files into a more structured layout.
"""
import os
import shutil
from pathlib import Path

def create_directories():
    """Create all necessary directories for the project."""
    dirs = [
        # Main directories
        'app/config',
        'app/models',
        'app/routes/api/v1/endpoints',
        'app/static/css',
        'app/static/js',
        'app/static/images',
        'app/templates/auth',
        'app/templates/main',
        'app/utils',
        'data/raw',
        'data/processed',
        'data/external',
        'tests/unit',
        'tests/integration',
        'docs/api',
        'docs/deployment',
        'docs/development',
        'scripts/debug',
        'scripts/maintenance',
        'scripts/database',
        'scripts/analysis'
    ]
    
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
        # Create __init__.py in Python packages
        if directory.startswith(('app/', 'scripts/')):
            Path(directory).joinpath('__init__.py').touch(exist_ok=True)

def move_files():
    """Move files to their new locations."""
    root = Path('.')
    
    # Define file movements as (source, destination) tuples
    movements = [
        # Configuration
        ('config.py', 'app/config/settings.py'),
        
        # Scripts
        ('comprehensive_system_check.py', 'scripts/debug/system_check.py'),
        ('debug_app.py', 'scripts/debug/app_debug.py'),
        ('fix_users.py', 'scripts/maintenance/fix_users.py'),
        ('init_db.py', 'scripts/database/init_db.py'),
        ('reorganize_project.py', 'scripts/maintenance/reorganize_project.py'),
        ('visualization_script.py', 'scripts/analysis/visualization.py'),
        
        # Documentation
        ('FINAL_VERIFICATION_REPORT.md', 'docs/development/FINAL_VERIFICATION.md'),
        ('FIXES_IMPLEMENTATION_REPORT.md', 'docs/development/FIXES_IMPLEMENTATION.md'),
        ('INTEGRATION_REPORT.md', 'docs/development/INTEGRATION_REPORT.md'),
        ('REQUIREMENTS.md', 'docs/development/REQUIREMENTS.md'),
        ('RUNNING_GUIDE.md', 'docs/development/RUNNING_GUIDE.md'),
        
        # Test files
        ('test_*.py', 'tests/unit/'),
        
        # Data files
        ('crime_hotspot.db', 'data/development.db'),
    ]
    
    for src_pattern, dest in movements:
        # Handle wildcard patterns
        if '*' in src_pattern:
            for src_file in root.glob(src_pattern):
                if src_file.is_file():
                    dest_path = Path(dest) / src_file.name if dest.endswith('/') else Path(dest)
                    shutil.move(str(src_file), str(dest_path))
                    print(f"Moved: {src_file} -> {dest_path}")
        else:
            src = Path(src_pattern)
            if src.exists():
                dest_path = Path(dest)
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dest_path))
                print(f"Moved: {src} -> {dest_path}")

def update_references():
    """Update file references in the codebase."""
    # Update imports in Python files
    for py_file in Path('.').rglob('*.py'):
        try:
            content = py_file.read_text()
            
            # Update imports and references
            updates = {
                'from app.config import settings as config': 'from app.config import settings as config',
                'from app.config.settings import': 'from app.config.settings import',
                'from scripts.debug.app_debug import': 'from scripts.debug.app_debug import',
                'from scripts.database.init_db import': 'from scripts.database.init_db import',
                'from scripts.maintenance.fix_users import': 'from scripts.maintenance.fix_users import',
                'from scripts.analysis.visualization import': 'from scripts.analysis.visualization import',
                "app/static/uploads/": "app/static/uploads/",  # No change, just an example
            }
            
            for old, new in updates.items():
                content = content.replace(old, new)
                
            # Update test imports
            if str(py_file).startswith('tests/'):
                content = content.replace('from test_', 'from tests.unit.test_')
                
            py_file.write_text(content)
            print(f"Updated references in: {py_file}")
            
        except Exception as e:
            print(f"Error updating {py_file}: {e}")

def secure_sensitive_info():
    """Secure sensitive information in configuration files."""
    # Create .env file if it doesn't exist
    if not Path('.env').exists():
        shutil.copy('.env.example', '.env')
    
    # Add .env to .gitignore if not already present
    gitignore = Path('.gitignore')
    if gitignore.exists():
        gitignore_content = gitignore.read_text()
        if '.env' not in gitignore_content:
            with gitignore.open('a') as f:
                f.write('\n# Environment variables\n.env\n')
    
    # Update .env.example with placeholders
    if Path('.env.example').exists():
        content = Path('.env.example').read_text()
        
        # Replace sensitive values with placeholders
        sensitive = {
            'kmd.zaheer2006@gmail.com': 'your-email@example.com',
            '244343': 'your-email-password',
            'your-mapbox-token-here': 'your-mapbox-token-here',
            'your-google-maps-api-key': 'your-google-maps-api-key',
            'your-password-salt-here': 'your-password-salt-here',
            'your-google-client-id': 'your-google-client-id',
            'your-google-client-secret': 'your-google-client-secret',
            'your-facebook-app-id': 'your-facebook-app-id',
            'your-facebook-app-secret': 'your-facebook-app-secret'
        }
        
        for old, new in sensitive.items():
            content = content.replace(old, new)
            
        Path('.env.example').write_text(content)
        print("Secured sensitive information in .env.example")

def main():
    print("🚀 Starting project reorganization...")
    
    print("\n📂 Creating directory structure...")
    create_directories()
    
    print("\n📦 Moving files to new locations...")
    move_files()
    
    print("\n🔄 Updating file references...")
    update_references()
    
    print("\n🔒 Securing sensitive information...")
    secure_sensitive_info()
    
    print("\n✅ Project reorganization complete!")
    print("\nNext steps:")
    print("1. Review the changes in git")
    print("2. Test the application to ensure everything works")
    print("3. Update any remaining hardcoded paths in your code")
    print("4. Commit the changes to version control")

if __name__ == "__main__":
    main()
