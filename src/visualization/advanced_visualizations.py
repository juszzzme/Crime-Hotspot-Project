"""
Advanced Visualization Script for Crime Data Analysis

This script generates various advanced visualizations for crime data analysis,
including temporal patterns, geospatial heatmaps, and statistical relationships.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style for visualizations
plt.style.use('ggplot')
sns.set_theme(style="whitegrid")
plt.rcParams['figure.facecolor'] = 'white'

# Constants
# Using absolute path to avoid path resolution issues
PROJECT_ROOT = Path(__file__).parent.parent.parent  # Go up three levels to reach project root
DATA_DIR = PROJECT_ROOT / "data" / "raw" / "ncrb" / "district_wise" / "vulnerable_groups"
OUTPUT_DIR = PROJECT_ROOT / "reports" / "figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_data():
    """Load and preprocess the crime data."""
    try:
        # Load women's crime data from NCRB
        women_crime_file = DATA_DIR / "42_District_wise_crimes_committed_against_women_2014.csv"
        print(f"Current working directory: {os.getcwd()}")
        print(f"Full path to file: {os.path.abspath(women_crime_file)}")
        print(f"File exists: {os.path.exists(women_crime_file)}")
        print(f"Loading data from: {women_crime_file}")
        df = pd.read_csv(women_crime_file, encoding='latin1')
        
        # Basic preprocessing
        df = df.dropna()
        # Convert state names to title case for better readability
        if 'State/UT' in df.columns:
            df['State/UT'] = df['State/UT'].str.title()
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def plot_temporal_trends(df):
    """Plot temporal trends in crime data."""
    if 'Year' not in df.columns:
        print("No 'Year' column found for temporal analysis")
        return
    
    plt.figure(figsize=(14, 7))
    yearly_data = df.groupby('Year').sum(numeric_only=True).reset_index()
    
    # Select top 5 crime types by total count
    crime_cols = [col for col in yearly_data.columns if col not in ['Year', 'Total']]
    top_crimes = yearly_data[crime_cols].sum().sort_values(ascending=False).head(5).index
    
    for crime in top_crimes:
        plt.plot(yearly_data['Year'], yearly_data[crime], marker='o', label=crime)
    
    plt.title('Temporal Trends in Crime (Top 5 Categories)', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Number of Reported Cases', fontsize=14)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Save the figure
    output_path = OUTPUT_DIR / 'temporal_trends.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Temporal trends plot saved to: {output_path}")

def plot_geographic_heatmap(df):
    """Create a heatmap of crime distribution by state/UT."""
    if 'State/UT' not in df.columns:
        print("No 'State/UT' column found for geographic analysis")
        return
    
    # Aggregate data by state
    state_data = df.groupby('State/UT').sum(numeric_only=True).reset_index()
    
    # Select top 10 states by total crimes
    state_data = state_data.nlargest(10, 'Total') if 'Total' in state_data.columns else state_data
    
    # Prepare data for heatmap (excluding non-numeric columns)
    numeric_cols = state_data.select_dtypes(include=[np.number]).columns
    heatmap_data = state_data[numeric_cols].transpose()
    
    plt.figure(figsize=(14, 10))
    sns.heatmap(heatmap_data, 
                cmap='YlOrRd',
                annot=True, 
                fmt='.0f',
                linewidths=0.5,
                cbar_kws={'label': 'Number of Cases'})
    
    plt.title('Crime Distribution by State (Top 10)', fontsize=16)
    plt.xlabel('State/UT', fontsize=14)
    plt.ylabel('Crime Type', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Save the figure
    output_path = OUTPUT_DIR / 'geographic_heatmap.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Geographic heatmap saved to: {output_path}")

def plot_crime_correlations(df):
    """
    Plot correlation matrix of different crime types.
    """
    # Select only numeric columns for correlation
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) < 2:
        print("Not enough numeric columns for correlation analysis")
        return
    
    # Calculate correlation matrix
    corr = df[numeric_cols].corr()
    
    # Create a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    plt.figure(figsize=(14, 12))
    sns.heatmap(corr, 
                mask=mask,
                cmap='coolwarm',
                center=0,
                square=True,
                linewidths=0.5,
                cbar_kws={"shrink": .8})
    
    plt.title('Correlation Between Different Crime Types', fontsize=16)
    plt.tight_layout()
    
    # Save the figure
    output_path = OUTPUT_DIR / 'crime_correlations.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Correlation matrix saved to: {output_path}")

def main():
    print("Starting advanced visualizations...")
    
    # Load the data
    df = load_data()
    if df is None or df.empty:
        print("No data loaded. Exiting.")
        return
    
    print(f"Loaded data with {len(df)} rows and {len(df.columns)} columns")
    
    # Generate visualizations
    plot_temporal_trends(df)
    plot_geographic_heatmap(df)
    plot_crime_correlations(df)
    
    print("\nAdvanced visualizations completed!")

if __name__ == "__main__":
    main()
