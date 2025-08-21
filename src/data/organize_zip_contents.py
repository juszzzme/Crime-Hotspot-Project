import os
import shutil
from pathlib import Path

def organize_zip_contents():
    # Base directories
    base_dir = Path.cwd()
    temp_dir = base_dir / "temp_extract"
    
    # Target directories
    ncrb_dir = base_dir / "data" / "raw" / "ncrb"
    ncrb_csv_dir = ncrb_dir / "csv"
    
    # Create target directories if they don't exist
    ncrb_csv_dir.mkdir(parents=True, exist_ok=True)
    
    # List of files to organize
    csv_files = [
        "10_Property_stolen_and_recovered.csv",
        "20_Victims_of_rape.csv",
        "25_Complaints_against_police.csv",
        "28_Trial_of_violent_crimes_by_courts.csv",
        "29_Period_of_trials_by_courts.csv",
        "30_Auto_theft.csv",
        "31_Serious_fraud.csv",
        "32_Murder_victim_age_sex.csv",
        "33_CH_not_murder_victim_age_sex.csv",
        "35_Human_rights_violation_by_police.csv",
        "36_Police_housing.csv",
        "39_Specific_purpose_of_kidnapping_and_abduction.csv",
        "40_01_Custodial_death_person_remanded.csv",
        "40_02_Custodial_death_person_not_remanded.csv",
        "40_03_Custodial_death_during_production.csv",
        "40_04_Custodial_death_during_hospitalization_or_treatment.csv",
        "40_05_Custodial_death_others.csv",
        "42_Cases_under_crime_against_women.csv",
        "43_Arrests_under_crime_against_women.csv"
    ]
    
    # Move files to NCRB CSV directory
    for csv_file in csv_files:
        src = temp_dir / csv_file
        dst = ncrb_csv_dir / csv_file
        if src.exists():
            shutil.copy2(src, dst)
            print(f"Copied: {src} -> {dst}")
    
    # Check for the 'crime' directory
    crime_dir = temp_dir / "crime"
    if crime_dir.exists():
        print("\nFound 'crime' directory with additional files.")
        print("Please let me know how you'd like to organize these files.")
    
    print("\nFile organization complete!")
    print(f"CSV files have been moved to: {ncrb_csv_dir}")

if __name__ == "__main__":
    print("Organizing extracted ZIP contents...")
    organize_zip_contents()
