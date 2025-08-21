"""
Project Reorganization Script
============================

This script reorganizes the project structure for better maintainability.
It creates a logical directory structure and moves files to their appropriate locations.
"""

import os
import shutil
from pathlib import Path
import json

# Define the new directory structure
NEW_STRUCTURE = {
    "data": {
        "raw": {
            "ncrb_pdfs": "Original NCRB PDF files",
            "police_reports": "CSV/Excel files from police departments",
            "geographic": "Shapefiles and GeoJSON data"
        },
        "interim": {
            "extracted_tables": "Extracted tables from PDFs",
            "converted_data": "Converted/processed data files"
        },
        "processed": {
            "by_crime_type": {
                "against_women": "Crime data related to women",
                "against_children": "Crime data related to children",
                "against_sc_st": "Crime data related to SC/ST communities"
            },
            "by_geography": {
                "national": "National level aggregated data",
                "state": "State level data",
                "district": "District level data",
                "city": "City level data"
            },
            "time_series": "Time series data across years"
        }
    },
    "docs": {
        "reports": "Generated reports and documentation",
        "presentations": "Presentation materials"
    },
    "notebooks": {
        "exploratory": "Jupyter notebooks for data exploration",
        "analysis": "Jupyter notebooks for analysis"
    },
    "src": {
        "data": "Data processing scripts",
        "visualization": "Data visualization scripts",
        "models": "Model training and evaluation scripts",
        "utils": "Utility functions and helpers"
    },
    "reports": {
        "figures": "Generated figures and visualizations",
        "tables": "Generated tables and statistics"
    },
    "config": "Configuration files",
    "tests": "Test files"
}

def create_directory_structure(base_path, structure, level=0):
    """Create the directory structure."""
    for name, content in structure.items():
        path = base_path / name
        print(f"{'  ' * level}Creating: {path}")
        
        # Create directory if it doesn't exist
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            
        # Create README.md for the directory
        readme_path = path / "README.md"
        if not readme_path.exists():
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(f"# {name.replace('_', ' ').title()}\n\n")
                if isinstance(content, dict) and all(isinstance(v, str) for v in content.values()):
                    f.write("## Description\n\n")
                    for sub_name, desc in content.items():
                        f.write(f"- `{sub_name}`: {desc}\n")
        
        # Recursively create subdirectories
        if isinstance(content, dict):
            create_directory_structure(path, content, level + 1)

def move_files_to_new_structure():
    """Move existing files to the new structure."""
    # Mapping of file patterns to destination directories
    file_mapping = {
        "data/processed/by_crime_type/processed_42_*": "data/processed/by_crime_type/against_women/",
        "data/processed/by_crime_type/processed_03_*": "data/processed/by_crime_type/against_children/",
        "data/processed/by_crime_type/processed_02_*": "data/processed/by_crime_type/against_sc_st/",
        "data/processed/by_crime_type/processed_01_*": "data/processed/by_geography/district/",
        "data/processed/by_crime_type/processing_summary.json": "data/processed/",
        "data/processed/by_crime_type/filtered_out/*": "data/processed/filtered_out/",
        "reports/figures/*": "reports/figures/",
        "*.py": "src/data/",
        "*.ipynb": "notebooks/exploratory/",
        "*.md": "docs/"
    }
    
    # Create a mapping of source to destination
    for pattern, dest_dir in file_mapping.items():
        dest_path = Path(dest_dir)
        dest_path.mkdir(parents=True, exist_ok=True)
        
        # Find all files matching the pattern
        for src_file in Path(".").glob(pattern):
            if src_file.is_file():
                dest_file = dest_path / src_file.name
                print(f"Moving {src_file} to {dest_file}")
                shutil.move(str(src_file), str(dest_file))

def update_project_structure_guide():
    """Update the PROJECT_STRUCTURE_GUIDE.md with the new structure."""
    guide_path = Path("PROJECT_STRUCTURE_GUIDE.md")
    if guide_path.exists():
        with open(guide_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Find the section to update
        start_marker = "<!-- STRUCTURE_START -->"
        end_marker = "<!-- STRUCTURE_END -->"
        
        # Generate the new structure section
        new_section = generate_structure_section()
        
        # Replace the old section with the new one
        new_content = content.split(start_marker)[0] + start_marker + "\n" + new_section + "\n" + end_marker + content.split(end_marker)[1]
        
        with open(guide_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        
        print(f"Updated {guide_path}")

def generate_structure_section():
    """Generate the project structure section for the guide."""
    structure_md = "## Project Structure\n\n"
    structure_md += "```\n"
    
    def add_to_structure(base_path, level=0):
        nonlocal structure_md
        indent = "    " * level
        for item in sorted(base_path.iterdir()):
            if item.is_dir() and not item.name.startswith('.'):
                structure_md += f"{indent}{item.name}/\n"
                add_to_structure(item, level + 1)
            elif item.suffix in ['.py', '.ipynb', '.md', '.json', '.csv']:
                structure_md += f"{indent}{item.name}\n"
    
    # Create a temporary directory to generate the structure
    with open("temp_structure.json", "w", encoding="utf-8") as f:
        json.dump(NEW_STRUCTURE, f, indent=2)
    
    structure_md += "/ (project root)\n"
    for root, dirs, files in os.walk("."):
        level = root.replace(".", "").count(os.sep)
        indent = "    " * (level)
        structure_md += "{}{}/\n".format(indent, os.path.basename(root) if root != "." else "/")
        subindent = "    " * (level + 1)
        for f in files:
            if not f.startswith('.'):
                structure_md += "{}{}\n".format(subindent, f)
    
    structure_md += "```\n\n"
    
    # Add descriptions
    structure_md += "### Key Directories\n\n"
    structure_md += "- `data/`: Contains all data files in a structured format\n"
    structure_md += "  - `raw/`: Original data files (PDFs, CSVs, etc.)\n"
    structure_md += "  - `interim/`: Intermediate files during processing\n"
    structure_md += "  - `processed/`: Cleaned and processed data ready for analysis\n"
    structure_md += "- `docs/`: Documentation and reports\n"
    structure_md += "- `notebooks/`: Jupyter notebooks for exploration and analysis\n"
    structure_md += "- `reports/`: Generated reports and visualizations\n"
    structure_md += "- `src/`: Source code for data processing and analysis\n"
    
    return structure_md

def main():
    print("Reorganizing project structure...\n")
    
    # Create the new directory structure
    base_path = Path(".")
    create_directory_structure(base_path, NEW_STRUCTURE)
    
    # Move existing files to the new structure
    print("\nMoving files to new structure...")
    move_files_to_new_structure()
    
    # Update the project structure guide
    print("\nUpdating project structure guide...")
    update_project_structure_guide()
    
    print("\nReorganization complete!")
    print("Please review the changes and update any file paths in your code as needed.")

if __name__ == "__main__":
    main()
