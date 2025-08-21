"""
Crime Data Visualization Script
==============================

This script generates various visualizations from the preprocessed crime data.
It creates bar plots, line charts, and heatmaps to analyze crime patterns.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set up visualization style
plt.style.use('ggplot')
sns.set_theme(style="whitegrid")
sns.set_palette("viridis")

# Configuration
DATA_DIR = Path("data/processed/cleaned_data")
OUTPUT_DIR = Path("analysis/figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_women_crime_data():
    """Load the women's crime dataset."""
    try:
        # Load the most recent women's crime data
        file_path = DATA_DIR / "processed_42_District_wise_crimes_committed_against_women_2014.csv"
        df = pd.read_csv(file_path)
        
        # Basic cleaning
        df['district'] = df['district'].str.title().str.strip()
        
        # Calculate total crimes
        crime_columns = ['rape', 'murder', 'robbery', 'arson']
        df['total_crimes'] = df[crime_columns].sum(axis=1)
        
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def plot_crime_distribution(df):
    """Create a bar plot showing the distribution of different crime types."""
    crime_columns = ['rape', 'murder', 'robbery', 'arson']
    crime_sums = df[crime_columns].sum()
    
    plt.figure(figsize=(12, 6))
    ax = crime_sums.plot(kind='bar')
    
    # Add value labels on top of bars
    for i, v in enumerate(crime_sums):
        ax.text(i, v + 10, f"{v:,}", ha='center', fontweight='bold')
    
    plt.title('Distribution of Crime Types (2014)', fontsize=14, pad=20)
    plt.xlabel('Crime Type', labelpad=10)
    plt.ylabel('Number of Incidents', labelpad=10)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Save the figure
    output_path = OUTPUT_DIR / 'crime_distribution_2014.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_path

def plot_top_districts(df, crime_type='total_crimes', top_n=15):
    """Create a horizontal bar plot of top districts by crime type."""
    # Sort and select top districts
    top_districts = df.nlargest(top_n, crime_type)[['district', crime_type]].sort_values(crime_type)
    
    plt.figure(figsize=(12, 8))
    ax = sns.barplot(data=top_districts, x=crime_type, y='district')
    
    # Add value labels on bars
    for i, v in enumerate(top_districts[crime_type]):
        ax.text(v + 10, i, f"{v:,}", va='center', fontweight='bold')
    
    title = f'Top {top_n} Districts by {crime_type.replace("_", " ").title()} (2014)'
    plt.title(title, fontsize=14, pad=20)
    plt.xlabel('Number of Incidents', labelpad=10)
    plt.ylabel('District', labelpad=10)
    plt.tight_layout()
    
    # Save the figure
    output_path = OUTPUT_DIR / f'top_districts_{crime_type}_2014.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_path

def plot_crime_correlation(df):
    """Create a heatmap showing correlations between different crime types."""
    crime_columns = ['rape', 'murder', 'robbery', 'arson']
    
    # Calculate correlation matrix
    correlation_matrix = df[crime_columns].corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        correlation_matrix, 
        annot=True, 
        cmap='coolwarm', 
        center=0,
        fmt=".2f",
        linewidths=0.5,
        annot_kws={"size": 12}
    )
    
    plt.title('Correlation Between Different Crime Types (2014)', fontsize=14, pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Save the figure
    output_path = OUTPUT_DIR / 'crime_correlation_heatmap_2014.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_path

def main():
    print("Starting crime data visualization...")
    
    # Load the data
    df = load_women_crime_data()
    if df is None:
        print("Error: Could not load the data. Please check the file paths.")
        return
    
    print(f"\nLoaded data with {len(df)} districts")
    print("Sample data:")
    print(df.head())
    
    # Create visualizations
    print("\nCreating visualizations...")
    
    # 1. Crime distribution
    dist_path = plot_crime_distribution(df)
    print(f"- Created crime distribution plot: {dist_path}")
    
    # 2. Top districts by total crimes
    top_total_path = plot_top_districts(df, 'total_crimes')
    print(f"- Created top districts by total crimes: {top_total_path}")
    
    # 3. Top districts by rape cases
    top_rape_path = plot_top_districts(df, 'rape')
    print(f"- Created top districts by rape cases: {top_rape_path}")
    
    # 4. Crime correlation heatmap
    corr_path = plot_crime_correlation(df)
    print(f"- Created crime correlation heatmap: {corr_path}")
    
    print("\nVisualization complete! Check the 'analysis/figures' directory for outputs.")

if __name__ == "__main__":
    main()
