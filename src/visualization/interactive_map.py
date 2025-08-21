"""
Interactive Map for Crime Hotspot Visualization

This script creates an interactive map of India showing crime data using Folium.
It uses local GeoJSON files for state boundaries and overlays crime data.
"""
import os
import json
import folium
import pandas as pd
import geopandas as gpd
from pathlib import Path

# Set up paths
project_root = Path(__file__).parent.parent.parent
data_dir = project_root / 'data'
geo_data_dir = data_dir / 'raw' / 'geographic'
output_dir = project_root / 'reports' / 'maps'
output_dir.mkdir(parents=True, exist_ok=True)

def create_interactive_map():
    """Create an interactive map of India with crime data visualization."""
    print("Creating interactive map...")
    
    # Load India states GeoJSON
    states_geojson = geo_data_dir / 'maps' / 'INDIA_STATES.geojson'
    if not states_geojson.exists():
        print(f"Error: GeoJSON file not found at {states_geojson}")
        return
    
    # Load crime data (example - replace with your actual crime data)
    crime_data_path = data_dir / 'raw' / 'ncrb' / 'district_wise' / 'vulnerable_groups' / '42_District_wise_crimes_committed_against_women_2014.csv'
    
    try:
        # Read the GeoJSON file
        india_states = gpd.read_file(states_geojson)
        
        # Read crime data (example - you'll need to adjust this based on your data)
        if crime_data_path.exists():
            crime_data = pd.read_csv(crime_data_path, encoding='latin1')
            print(f"Loaded crime data with {len(crime_data)} records")
            # Here you would merge crime data with geo data based on common keys
            # For now, we'll just use the GeoJSON data
        
        # Create a base map centered on India
        m = folium.Map(
            location=[20.5937, 78.9629],  # Center of India
            zoom_start=5,
            tiles='cartodbpositron'  # Light map style (no API key needed)
        )
        
        # Print available fields for debugging
        print("\nAvailable fields in GeoJSON:")
        print(india_states.columns.tolist())
        
        # Add state boundaries with hover information
        folium.GeoJson(
            india_states,
            name='India States',
            style_function=lambda feature: {
                'fillColor': '#1f77b4',  # Blue color
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.7
            },
            tooltip=folium.GeoJsonTooltip(
                fields=['STNAME'],  # Using the correct field name
                aliases=['State: '],
                localize=True,
                style=("""
                    background-color: white;
                    color: #333333;
                    font-family: arial;
                    font-size: 12px;
                    padding: 2px;
                """)
            )
        ).add_to(m)
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        # Save the map to an HTML file
        output_file = output_dir / 'india_crime_map.html'
        m.save(str(output_file))
        print(f"Interactive map saved to: {output_file}")
        
        return str(output_file)
        
    except Exception as e:
        print(f"Error creating map: {str(e)}")
        return None

if __name__ == "__main__":
    map_file = create_interactive_map()
    if map_file:
        print(f"Map generation successful! Open {map_file} in a web browser to view.")
    else:
        print("Failed to generate the map. Please check the error messages above.")
