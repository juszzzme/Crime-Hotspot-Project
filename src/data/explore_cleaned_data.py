"""
Crime Data Exploration Script
============================

This script explores the cleaned crime data to understand patterns and trends.
It creates visualizations and generates insights from the processed data.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set up visualization style
plt.style.use('ggplot')  # Using a built-in style instead of seaborn
sns.set_theme(style="whitegrid")  # Using seaborn's whitegrid theme
sns.set_palette("viridis")

# Configuration
DATA_DIR = Path("data/processed/cleaned_data")
OUTPUT_DIR = Path("analysis/figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_processed_data():
    """Load all processed data files."""
    data_files = list(DATA_DIR.glob("*.csv"))
    print(f"Found {len(data_files)} processed data files")
    
    # Dictionary to store DataFrames
    dfs = {}
    
    for file in data_files:
        try:
            df_name = file.stem.replace("processed_", "")
            dfs[df_name] = pd.read_csv(file)
            print(f"Loaded {file.name} with shape {dfs[df_name].shape}")
        except Exception as e:
            print(f"Error loading {file}: {e}")
    
    return dfs

def explore_crime_patterns(dfs):
    """Explore patterns in the crime data."""
    # Find files containing crime data
    crime_files = {k: v for k, v in dfs.items() if 'crime' in k.lower()}
    
    for name, df in crime_files.items():
        print(f"\nAnalyzing {name}...")
        print("-" * 50)
        
        # Basic info
        print("\nDataFrame Info:")
        print(f"Shape: {df.shape}")
        print("\nFirst few rows:")
        print(df.head())
        
        # Check for state and district columns
        has_state = 'state' in df.columns
        has_district = 'district' in df.columns
        
        # Basic statistics for numerical columns
        print("\nNumerical Columns Summary:")
        num_cols = df.select_dtypes(include=['int64', 'float64']).columns
        if len(num_cols) > 0:
            print(df[num_cols].describe())
        
        # If state data is available, analyze by state
        if has_state:
            print("\nTop 5 States by Crime Count:")
            state_counts = df['state'].value_counts().head()
            print(state_counts)
            
            # Plot top states
            if len(state_counts) > 0:
                plt.figure(figsize=(12, 6))
                state_counts.plot(kind='bar')
                plt.title(f'Top 5 States by Crime Count - {name}')
                plt.xlabel('State')
                plt.ylabel('Number of Crime Records')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.savefig(OUTPUT_DIR / f'top_states_{name}.png')
                plt.close()
        
        # If district data is available, analyze by district
        if has_district and has_state:
            print("\nTop 5 Districts by Crime Count:")
            district_counts = df.groupby(['state', 'district']).size().sort_values(ascending=False).head()
            print(district_counts)
            
            # Plot top districts
            if len(district_counts) > 0:
                plt.figure(figsize=(12, 6))
                district_counts.plot(kind='bar')
                plt.title(f'Top 5 Districts by Crime Count - {name}')
                plt.xlabel('(State, District)')
                plt.ylabel('Number of Crime Records')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                plt.savefig(OUTPUT_DIR / f'top_districts_{name}.png')
                plt.close()
        
        # Time-based analysis if year column exists
        if 'year' in df.columns:
            print("\nCrime Trends Over Time:")
            yearly_counts = df['year'].value_counts().sort_index()
            print(yearly_counts)
            
            plt.figure(figsize=(12, 6))
            yearly_counts.plot(kind='line', marker='o')
            plt.title(f'Crime Trends Over Time - {name}')
            plt.xlabel('Year')
            plt.ylabel('Number of Crime Records')
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(OUTPUT_DIR / f'trends_{name}.png')
            plt.close()

def main():
    print("Starting crime data exploration...")
    
    # Load all processed data
    dfs = load_processed_data()
    
    if not dfs:
        print("No data files found. Please run the data processing scripts first.")
        return
    
    # Explore crime patterns
    explore_crime_patterns(dfs)
    
    print("\nExploration complete! Check the 'analysis/figures' directory for visualizations.")

if __name__ == "__main__":
    main()
