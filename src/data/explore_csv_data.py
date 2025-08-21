import os
import pandas as pd
from pathlib import Path

def explore_csv_files(directory):
    """
    Explore CSV files in the given directory and its subdirectories.
    Print basic information about each CSV file.
    """
    # Find all CSV files in the directory and subdirectories
    csv_files = list(Path(directory).rglob('*.csv'))
    
    print(f"Found {len(csv_files)} CSV files in {directory}")
    
    # Dictionary to store information about the CSV files
    csv_info = []
    
    # Analyze each CSV file
    for csv_file in csv_files:
        try:
            # Read the CSV file
            df = pd.read_csv(csv_file, nrows=5)  # Read only first 5 rows for efficiency
            
            # Get file info
            file_info = {
                'file_path': str(csv_file.relative_to(directory)),
                'file_size_mb': os.path.getsize(csv_file) / (1024 * 1024),  # Size in MB
                'num_columns': len(df.columns),
                'num_rows': sum(1 for _ in open(csv_file, 'r', encoding='utf-8', errors='ignore')) - 1,  # Subtract 1 for header
                'columns': list(df.columns),
                'first_few_rows': df.values.tolist()
            }
            
            csv_info.append(file_info)
            
        except Exception as e:
            print(f"Error reading {csv_file}: {str(e)}")
    
    return csv_info

def save_csv_summary(csv_info, output_file):
    """Save the CSV file information to a JSON file for reference."""
    import json
    
    # Create a simplified version for saving
    summary = []
    for info in csv_info:
        summary.append({
            'file_path': info['file_path'],
            'file_size_mb': info['file_size_mb'],
            'num_columns': info['num_columns'],
            'num_rows': info['num_rows'],
            'columns': info['columns']
        })
    
    # Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nCSV summary saved to {output_file}")

def find_csvs_with_keyword(csv_info, keyword):
    """Find CSV files that contain a specific keyword in their columns."""
    keyword = keyword.lower()
    matching_files = []
    
    for info in csv_info:
        # Check if keyword is in any column name
        columns_lower = [str(col).lower() for col in info['columns']]
        if any(keyword in col for col in columns_lower):
            matching_files.append({
                'file_path': info['file_path'],
                'matching_columns': [col for col in info['columns'] if keyword in str(col).lower()]
            })
    
    return matching_files

if __name__ == "__main__":
    # Directory containing the CSV files
    data_dir = "data/raw/ncrb_pdfs/ncrb"
    
    # Explore CSV files
    print(f"Exploring CSV files in {data_dir}...")
    csv_info = explore_csv_files(data_dir)
    
    # Save summary to file
    output_file = "data/processed/csv_summary.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    save_csv_summary(csv_info, output_file)
    
    # Find files related to specific keywords
    keywords = ['tamil', 'chennai', 'crime', 'state', 'district']
    
    print("\nSearching for files related to specific keywords:")
    for keyword in keywords:
        matching = find_csvs_with_keyword(csv_info, keyword)
        if matching:
            print(f"\nFiles containing '{keyword}':")
            for match in matching:
                print(f"- {match['file_path']} (Columns: {', '.join(match['matching_columns'])})")
        else:
            print(f"No files found containing '{keyword}'")
