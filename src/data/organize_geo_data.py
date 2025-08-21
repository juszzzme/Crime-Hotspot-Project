"""
Script to organize geographic data (Maps and Population) into the project structure.
"""
import os
import shutil
from pathlib import Path

def organize_geo_data():
    """Organize geographic data into the project structure."""
    # Define paths
    project_root = Path(__file__).parent.parent.parent
    maps_src = project_root / "Maps"
    pop_src = project_root / "Population density data"
    
    # Target directories
    geo_data_dir = project_root / "data" / "raw" / "geographic"
    maps_dir = geo_data_dir / "maps"
    population_dir = geo_data_dir / "population"
    
    # Create target directories if they don't exist
    for directory in [geo_data_dir, maps_dir, population_dir]:
        os.makedirs(directory, exist_ok=True)
    
    print("Organizing geographic data...")
    
    # Copy Maps data
    print("\nProcessing Maps data:")
    for item in maps_src.glob("*"):
        if item.is_file():
            print(f"Copying {item.name} to {maps_dir}")
            shutil.copy2(item, maps_dir / item.name)
    
    # Copy Population data
    print("\nProcessing Population data:")
    for item in pop_src.glob("*"):
        if item.is_file():
            print(f"Copying {item.name} to {population_dir}")
            shutil.copy2(item, population_dir / item.name)
    
    print("\nGeographic data organization complete!")
    print(f"Maps data location: {maps_dir}")
    print(f"Population data location: {population_dir}")

if __name__ == "__main__":
    organize_geo_data()
