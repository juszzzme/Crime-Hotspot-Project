import os
import shutil
from pathlib import Path

def organize_files():
    # Base directories
    base_dir = Path.cwd()
    crime_data_dir = base_dir / "crime data"
    
    # Target directories
    ncrb_dir = base_dir / "data" / "raw" / "ncrb"
    police_dir = base_dir / "data" / "raw" / "police"
    
    # Create target directories if they don't exist
    ncrb_dir.mkdir(parents=True, exist_ok=True)
    police_dir.mkdir(parents=True, exist_ok=True)
    
    # File mapping: source -> destination
    file_mapping = {
        # NCRB PDFs
        crime_data_dir / "crimeinIndia2022Book1.pdf": ncrb_dir / "crimeinIndia2022Book1.pdf",
        crime_data_dir / "TamilNadu Data" / "tn_cr_statistics_2022.pdf": ncrb_dir / "tn_cr_statistics_2022.pdf",
        
        # Police data (CSV files)
        crime_data_dir / "statewise crime data.csv": police_dir / "statewise_crime_data.csv",
        crime_data_dir / "cities crime dataset.csv": police_dir / "cities_crime_dataset.csv",
        crime_data_dir / "TamilNadu Data" / "DistrictwiseofTN.csv": police_dir / "tamilnadu_districtwise.csv",
        crime_data_dir / "TamilNadu Data" / "MurdercasesTN.csv": police_dir / "tamilnadu_murder_cases.csv"
    }
    
    # Move files to their new locations
    for src, dst in file_mapping.items():
        if src.exists():
            shutil.copy2(src, dst)
            print(f"Copied: {src} -> {dst}")
        else:
            print(f"Warning: Source file not found: {src}")
    
    # Handle ZIP file
    zip_file = crime_data_dir / "Crime data.zip"
    if zip_file.exists():
        print("\nFound ZIP file. Extracting to temporary directory...")
        temp_dir = base_dir / "temp_extract"
        temp_dir.mkdir(exist_ok=True)
        
        import zipfile
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        print(f"ZIP contents extracted to: {temp_dir}")
        print("Please check the contents and let me know how you'd like to organize them.")
    
    print("\nFile organization complete!")
    print("Please verify the files in the following directories:")
    print(f"- NCRB Data: {ncrb_dir}")
    print(f"- Police Data: {police_dir}")

if __name__ == "__main__":
    print("Starting data organization...")
    organize_files()
