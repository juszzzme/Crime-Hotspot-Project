"""
CRIME DATA CLEANING AND PREPROCESSING TUTORIAL
============================================

This script demonstrates how to clean and preprocess crime data from the NCRB (National Crime Records Bureau).
It includes functions for handling missing data, standardizing formats, and filtering relevant information.

Key Concepts:
1. Data Cleaning: Handling missing values, standardizing formats
2. Data Filtering: Selecting relevant columns and rows
3. Data Transformation: Converting data types, creating new features
4. Data Organization: Saving processed data in a structured way
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
import json

# ====================================
# 1. DATA CLEANING FUNCTIONS
# ====================================

def clean_column_names(df):
    """
    Standardize column names by:
    - Converting to lowercase
    - Replacing spaces with underscores
    - Removing special characters
    """
    df = df.copy()
    df.columns = (df.columns
                 .str.lower()
                 .str.replace(' ', '_')
                 .str.replace('.', '')
                 .str.replace('-', '_')
                 .str.strip())
    return df

def handle_missing_values(df, fill_strategy=0):
    """
    Handle missing values in the DataFrame.
    
    Args:
        df: Input DataFrame
        fill_strategy: Value to fill missing values with (default: 0)
                      Can be 'mean', 'median', or a specific value
    """
    df = df.copy()
    
    # Convert numeric columns to numeric, coercing errors to NaN
    for col in df.select_dtypes(include=['object']).columns:
        try:
            df[col] = pd.to_numeric(df[col], errors='ignore')
        except:
            pass
    
    # Fill missing values based on strategy
    if fill_strategy in ['mean', 'median']:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if fill_strategy == 'mean':
                df[col] = df[col].fillna(df[col].mean())
            else:  # median
                df[col] = df[col].fillna(df[col].median())
    else:
        df = df.fillna(fill_strategy)
    
    return df

def standardize_state_names(df, state_col='state'):
    """Standardize state/UT names to a consistent format."""
    if state_col not in df.columns:
        return df
    
    df = df.copy()
    
    # Common state name mappings
    state_mapping = {
        'DELHI (UT)': 'DELHI',
        'A&N ISLANDS': 'ANDAMAN & NICOBAR ISLANDS',
        'D&N HAVELI': 'DADRA & NAGAR HAVELI',
        'DAMAN & DIU': 'DAMAN AND DIU',
        'JAMMU & KASHMIR': 'JAMMU AND KASHMIR',
        'TAMILNADU': 'TAMIL NADU',
        'PONDICHERRY': 'PUDUCHERRY',
        'ORISSA': 'ODISHA'
    }
    
    df[state_col] = (df[state_col]
                    .str.upper()
                    .str.strip()
                    .replace(state_mapping))
    
    return df

# ====================================
# 2. DATA FILTERING FUNCTIONS
# ====================================

def filter_by_states(df, states_to_keep, state_col='state'):
    """
    Filter DataFrame to include only specified states.
    
    Args:
        df: Input DataFrame
        states_to_keep: List of state names to include
        state_col: Name of the state column
    """
    if state_col not in df.columns:
        return df, pd.DataFrame()  # Return empty DataFrame for filtered out data
    
    # Convert to uppercase for case-insensitive comparison
    states_upper = [s.upper() for s in states_to_keep]
    
    # Create mask for rows to keep
    mask = df[state_col].str.upper().isin(states_upper)
    
    # Split into kept and filtered DataFrames
    kept_df = df[mask].copy()
    filtered_df = df[~mask].copy()
    
    return kept_df, filtered_df

def filter_by_columns(df, columns_to_keep):
    """
    Keep only specified columns in the DataFrame.
    
    Args:
        df: Input DataFrame
        columns_to_keep: List of column names to keep
    """
    # Find intersection of requested columns and actual columns
    columns_to_drop = [col for col in df.columns if col not in columns_to_keep]
    
    # Create copy with only kept columns
    kept_df = df.drop(columns=columns_to_drop, errors='ignore')
    
    # Create DataFrame with dropped columns
    filtered_df = df[columns_to_drop].copy()
    
    return kept_df, filtered_df

# ====================================
# 3. DATA PROCESSING PIPELINE
# ====================================

def process_crime_data(input_file, output_dir, states_to_keep=None, columns_to_keep=None):
    """
    Main function to process crime data.
    
    Args:
        input_file: Path to input CSV file
        output_dir: Directory to save processed files
        states_to_keep: List of states to include (None to keep all)
        columns_to_keep: List of columns to include (None to keep all)
    """
    # Create output directories
    os.makedirs(output_dir, exist_ok=True)
    filtered_dir = os.path.join(output_dir, 'filtered_out')
    os.makedirs(filtered_dir, exist_ok=True)
    
    # Generate output filenames
    input_filename = os.path.basename(input_file)
    base_filename = os.path.splitext(input_filename)[0]
    output_file = os.path.join(output_dir, f'processed_{base_filename}.csv')
    filtered_file = os.path.join(filtered_dir, f'filtered_{base_filename}.csv')
    
    # Read input file
    print(f"Processing {input_file}...")
    df = pd.read_csv(input_file)
    
    # Clean data
    df_clean = clean_column_names(df)
    df_clean = handle_missing_values(df_clean)
    df_clean = standardize_state_names(df_clean)
    
    # Initialize filtered data list
    filtered_data = []
    
    # Filter by states if specified
    if states_to_keep:
        df_clean, df_filtered = filter_by_states(df_clean, states_to_keep)
        if not df_filtered.empty:
            filtered_data.append(('states', df_filtered))
    
    # Filter by columns if specified
    if columns_to_keep:
        df_clean, df_filtered = filter_by_columns(df_clean, columns_to_keep)
        if not df_filtered.empty:
            filtered_data.append(('columns', df_filtered))
    
    # Save processed data
    df_clean.to_csv(output_file, index=False)
    print(f"Processed data saved to {output_file}")
    
    # Save filtered data if any
    if filtered_data:
        # Combine all filtered data
        all_filtered = pd.concat([df for _, df in filtered_data], axis=1)
        all_filtered.to_csv(filtered_file, index=False)
        print(f"Filtered data saved to {filtered_file}")
    
    return df_clean

# ====================================
# 4. EXAMPLE USAGE
# ====================================

if __name__ == "__main__":
    # Example configuration
    INPUT_FILE = "data/raw/ncrb_pdfs/ncrb/district_wise/district_crimes/01_District_wise_crimes_committed_IPC_2014.csv"
    OUTPUT_DIR = "data/processed/cleaned_data"
    
    # States of interest (focus on Tamil Nadu and neighboring states)
    TARGET_STATES = [
        'TAMIL NADU', 'KARNATAKA', 'KERALA', 'ANDHRA PRADESH', 'TELANGANA'
    ]
    
    # Columns to keep (example - adjust based on actual data)
    COLUMNS_TO_KEEP = [
        'state', 'district', 'murder', 'rape', 'kidnapping', 'robbery', 'theft'
    ]
    
    # Process the data
    processed_df = process_crime_data(
        input_file=INPUT_FILE,
        output_dir=OUTPUT_DIR,
        states_to_keep=TARGET_STATES,
        columns_to_keep=COLUMNS_TO_KEEP
    )
    
    # Display summary of processed data
    if not processed_df.empty:
        print("\nProcessing complete!")
        print(f"Number of rows: {len(processed_df)}")
        print(f"Number of columns: {len(processed_df.columns)}")
        print("\nFirst few rows:")
        print(processed_df.head())
    else:
        print("No data was processed. Please check the input file and parameters.")
