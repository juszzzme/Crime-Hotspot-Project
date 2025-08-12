"""
DATA FILTERING AND PROCESSING SCRIPT
==================================

This script processes crime data files, filters them based on specified criteria,
and saves both the processed data and filtered-out data separately.
"""

import os
import pandas as pd
from pathlib import Path
import json
from data_cleaning_tutorial import (
    clean_column_names,
    handle_missing_values,
    standardize_state_names,
    filter_by_states,
    filter_by_columns
)

# ====================================
# CONFIGURATION
# ====================================

# Define target states (focus on Tamil Nadu and neighboring states)
TARGET_STATES = [
    'TAMIL NADU', 'KARNATAKA', 'KERALA', 
    'ANDHRA PRADESH', 'TELANGANA', 'PUDUCHERRY'
]

# Define columns to keep (adjust based on your analysis needs)
COLUMNS_TO_KEEP = [
    'state', 'district', 'year', 'total_ipc_crimes',
    'murder', 'rape', 'kidnapping', 'robbery', 'theft',
    'dacoity', 'riots', 'cheating', 'counterfeiting',
    'arson', 'homicide', 'extortion'
]

# Define input and output directories
INPUT_DIR = "data/raw/ncrb/district_wise"
OUTPUT_DIR = "data/processed/cleaned_data"
FILTERED_DIR = os.path.join(OUTPUT_DIR, "filtered_out")

# Create output directories if they don't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FILTERED_DIR, exist_ok=True)

# ====================================
# PROCESSING FUNCTIONS
# ====================================

def process_file(file_path, output_dir, filtered_dir, target_states, columns_to_keep):
    """Process a single data file."""
    try:
        # Read the file
        df = pd.read_csv(file_path)
        
        # Clean the data
        df_clean = clean_column_names(df)
        df_clean = handle_missing_values(df_clean)
        df_clean = standardize_state_names(df_clean)
        
        # Add year if not present (extract from filename if possible)
        if 'year' not in df_clean.columns:
            try:
                year = int(''.join(filter(str.isdigit, os.path.basename(file_path)))[-4:])
                df_clean['year'] = year
            except:
                pass
        
        # Filter by states
        if target_states:
            df_clean, df_filtered_states = filter_by_states(df_clean, target_states)
            if not df_filtered_states.empty:
                filtered_states_file = os.path.join(
                    filtered_dir, 
                    f"filtered_states_{os.path.basename(file_path)}"
                )
                df_filtered_states.to_csv(filtered_states_file, index=False)
        
        # Filter by columns
        if columns_to_keep:
            # Get columns that actually exist in the DataFrame
            existing_columns = [col for col in columns_to_keep if col in df_clean.columns]
            df_clean, df_filtered_cols = filter_by_columns(df_clean, existing_columns)
            
            if not df_filtered_cols.empty:
                filtered_cols_file = os.path.join(
                    filtered_dir, 
                    f"filtered_columns_{os.path.basename(file_path)}"
                )
                df_filtered_cols.to_csv(filtered_cols_file, index=False)
        
        # Save the processed data
        output_file = os.path.join(
            output_dir, 
            f"processed_{os.path.basename(file_path)}"
        )
        df_clean.to_csv(output_file, index=False)
        
        return {
            'status': 'success',
            'file': file_path,
            'processed_rows': len(df_clean),
            'filtered_states': len(df) - len(df_clean) if target_states else 0,
            'filtered_columns': len(df_clean.columns) - len(existing_columns) if columns_to_keep else 0,
            'output_file': output_file
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'file': file_path,
            'error': str(e)
        }

def process_directory(input_dir, output_dir, filtered_dir, target_states=None, columns_to_keep=None):
    """Process all CSV files in the input directory."""
    # Find all CSV files in the directory and subdirectories
    csv_files = list(Path(input_dir).rglob('*.csv'))
    
    if not csv_files:
        print(f"No CSV files found in {input_dir}")
        return []
    
    print(f"Found {len(csv_files)} CSV files to process" if len(csv_files) > 1 else "Found 1 CSV file to process")
    
    # Process each file
    results = []
    for i, file_path in enumerate(csv_files, 1):
        print(f"\nProcessing file {i}/{len(csv_files)}: {file_path}")
        result = process_file(
            str(file_path), 
            output_dir, 
            filtered_dir,
            target_states,
            columns_to_keep
        )
        results.append(result)
        
        if result['status'] == 'success':
            print(f"  [DONE] Processed {result['processed_rows']} rows")
            print(f"  [SAVED] {result['output_file']}")
            if result.get('filtered_states', 0) > 0:
                print(f"  [FILTER] Removed {result['filtered_states']} rows (state filter)")
            if result.get('filtered_columns', 0) > 0:
                print(f"  [FILTER] Removed {result['filtered_columns']} columns")
        else:
            print(f"  [ERROR] {result.get('error', 'Unknown error')}")
    
    return results

def generate_summary(results, output_file):
    """Generate a summary of the processing results."""
    summary = {
        'total_files': len(results),
        'successful': sum(1 for r in results if r['status'] == 'success'),
        'failed': sum(1 for r in results if r['status'] == 'error'),
        'total_processed_rows': sum(r.get('processed_rows', 0) for r in results if r['status'] == 'success'),
        'total_filtered_states': sum(r.get('filtered_states', 0) for r in results if r['status'] == 'success'),
        'total_filtered_columns': sum(r.get('filtered_columns', 0) for r in results if r['status'] == 'success'),
        'failed_files': [r['file'] for r in results if r['status'] == 'error']
    }
    
    # Save summary to JSON
    with open(output_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    return summary

# ====================================
# MAIN EXECUTION
# ====================================

if __name__ == "__main__":
    # Set console encoding to UTF-8 if on Windows
    if os.name == 'nt':
        import sys
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    
    print("=" * 50)
    print("CRIME DATA PROCESSING SCRIPT")
    print("=" * 50)
    print(f"Input directory: {INPUT_DIR}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Filtered data directory: {FILTERED_DIR}")
    print(f"Target states: {', '.join(TARGET_STATES)}")
    print(f"Columns to keep: {', '.join(COLUMNS_TO_KEEP[:5])}..." if len(COLUMNS_TO_KEEP) > 5 else f"Columns to keep: {', '.join(COLUMNS_TO_KEEP)}")
    print("-" * 50)
    
    # Process all files in the input directory
    results = process_directory(
        INPUT_DIR, 
        OUTPUT_DIR, 
        FILTERED_DIR,
        target_states=TARGET_STATES,
        columns_to_keep=COLUMNS_TO_KEEP
    )
    
    # Generate and display summary
    summary_file = os.path.join(OUTPUT_DIR, 'processing_summary.json')
    summary = generate_summary(results, summary_file)
    
    print("\n" + "=" * 50)
    print("PROCESSING SUMMARY")
    print("=" * 50)
    print(f"Total files processed: {summary['total_files']}")
    print(f"Successfully processed: {summary['successful']}")
    print(f"Failed to process: {summary['failed']}")
    print(f"Total processed rows: {summary['total_processed_rows']:,}")
    print(f"Total rows filtered by state: {summary['total_filtered_states']:,}")
    print(f"Total columns filtered out: {summary['total_filtered_columns']}")
    print(f"\nSummary saved to: {summary_file}")
    
    if summary['failed_files']:
        print("\nFailed files:")
        for file in summary['failed_files']:
            print(f"  - {file}")
    
    print("\nProcessing complete!")
    print("=" * 50)
