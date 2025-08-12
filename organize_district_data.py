import os
import shutil
from pathlib import Path

def organize_district_data():
    # Base directories
    base_dir = Path.cwd()
    source_dir = base_dir / "temp_extract" / "crime"
    
    # Target directories
    target_base = base_dir / "data" / "raw" / "ncrb" / "district_wise"
    
    # Create target directories
    categories = {
        "district_crimes": ["01_District_wise_crimes_committed_"],
        "vulnerable_groups": ["02_01_District_wise_crimes_committed_against_SC", 
                             "02_District_wise_crimes_committed_against_ST",
                             "03_District_wise_crimes_committed_against_children",
                             "42_District_wise_crimes_committed_against_women"],
        "arrests_disposal": ["03_Persons_arrested_and_their_disposal",
                           "04_01_Person_arrested_and_their_disposal_by_police_and_court_SLL_crime",
                           "04_02_Person_arrested_and_their_disposal_by_police_and_court_IPC_crime"],
        "police_stats": ["11_Property_stolen_and_recovered_nature_of_property",
                       "12_Police_strength_actual_and_sanctioned",
                       "13_Police_killed_or_injured_on_duty",
                       "14_Age_profile_of_police_personnel_killed_on_duty",
                       "15_Police_natural_death_and_suicide",
                       "16_Casualties_under_police_firing_and_lathi_charge"],
        "juvenile_stats": ["08_01_Juvenile_apprehended_state_IPC",
                         "08_02_Juvenile_apprehended_state_SLL",
                         "09_Juveniles_arrested_and_their_disposal",
                         "18_01_Juveniles_arrested_Education",
                         "18_02_Juveniles_arrested_Economic_setup",
                         "18_03_Juveniles_arrested_Family_background",
                         "18_04_Juveniles_arrested_Recidivism"],
        "miscellaneous": ["17_Case_reported_and_value_of_property_taken_away_by_place_of_occurrence",
                         "17_Crime_by_place_of_occurrence",
                         "19_Motive_or_cause_of_murder_and_culpable_homicide_not_amounting_to_murder",
                         "21_Offenders_known_to_the_victim",
                         "22_Persons_arrested_under_recidivism",
                         "23_Anti_corruprion_cases",
                         "24_Anti_corruption_arrests",
                         "27_Nature_of_complaints_received_by_police",
                         "34_Use_of_fire_arms_in_murder_cases",
                         "37_Home_guards_and_auxilliary_force",
                         "38_Unidentified_dead_bodies_recovered_and_inquest_conducted",
                         "41_Escapes_from_police_custody"]
    }
    
    # Create all target directories
    for category in categories.keys():
        (target_base / category).mkdir(parents=True, exist_ok=True)
    
    # Move files to appropriate directories
    for file_path in source_dir.glob("*.csv"):
        file_name = file_path.name
        moved = False
        
        for category, patterns in categories.items():
            if any(pattern in file_name for pattern in patterns):
                dest = target_base / category / file_name
                shutil.copy2(file_path, dest)
                print(f"Copied: {file_name} -> {category}/")
                moved = True
                break
        
        if not moved:
            dest = target_base / "miscellaneous" / file_name
            shutil.copy2(file_path, dest)
            print(f"Copied (misc): {file_name} -> miscellaneous/")
    
    # Handle subdirectories (if any)
    for item in source_dir.iterdir():
        if item.is_dir() and item.name != "crime":  # Skip the 'crime' subdirectory to avoid recursion
            dest_dir = target_base / "additional_data" / item.name
            dest_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy all files from subdirectory
            for subfile in item.glob("*"):
                if subfile.is_file():
                    shutil.copy2(subfile, dest_dir / subfile.name)
                    print(f"Copied from subdir: {item.name}/{subfile.name} -> additional_data/{item.name}/")
    
    print("\nDistrict data organization complete!")
    print(f"Files have been organized in: {target_base}")

if __name__ == "__main__":
    print("Organizing district-level crime data...")
    organize_district_data()
