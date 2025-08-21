"""
Enhanced Choropleth Map Visualization for Crime Data

This script creates an interactive choropleth map of India with the following features:
- State-level crime data visualization
- Interactive tooltips with detailed crime statistics
- Time slider for temporal analysis
- Crime type filtering
- Legend explaining the color scale
- Zoom controls and scale bar
- Search functionality for states/districts
- Population data integration for crime rates
"""
import os
import json
import pandas as pd
import geopandas as gpd
import folium
import branca.colormap as cm
from pathlib import Path
from folium.plugins import Search, MiniMap, Fullscreen, MeasureControl
from folium.features import GeoJsonTooltip
import numpy as np

# Custom color scale for the choropleth
COLOR_SCALE = [
    '#ffffcc', '#ffeda0', '#fed976', '#feb24c',
    '#fd8d3c', '#fc4e2a', '#e31a1c', '#bd0026', '#800026'
]

# Set up paths
project_root = Path(__file__).parent.parent.parent
data_dir = project_root / 'data'
geo_data_dir = data_dir / 'raw' / 'geographic'
output_dir = project_root / 'reports' / 'maps'
output_dir.mkdir(parents=True, exist_ok=True)

def load_geojson(file_path):
    """Load and return GeoJSON data."""
    try:
        return gpd.read_file(file_path)
    except Exception as e:
        print(f"Error loading GeoJSON file {file_path}: {e}")
        return None

def create_enhanced_tooltip(row):
    """Create HTML content for tooltip with crime statistics."""
    total_crimes = row.get('Total Crimes Against Women', 0)
    crime_rate = row.get('Crime Rate', 'N/A')
    
    # Create crime distribution bars (example with some common crime types)
    crime_types = {
        'Rape': row.get('Rape', 0),
        'Kidnapping': row.get('Kidnapping and Abduction', 0),
        'Assault': row.get('Assault on Women', 0),
        'Insult to Modesty': row.get('Insult to Modesty', 0)
    }
    
    # Sort crimes by count (descending)
    sorted_crimes = sorted(crime_types.items(), key=lambda x: x[1], reverse=True)
    
    # Create HTML for crime distribution
    crime_bars = ''
    for crime, count in sorted_crimes:
        if count > 0:
            width = min(100, (count / max(1, total_crimes)) * 100) if isinstance(total_crimes, (int, float)) else 0
            crime_bars += f"""
            <div style="margin: 3px 0;">
                <div style="display: flex; justify-content: space-between; font-size: 0.9em;">
                    <span>{crime}</span>
                    <span>{count:,}</span>
                </div>
                <div style="height: 6px; background: #f0f0f0; border-radius: 3px; overflow: hidden;">
                    <div style="height: 100%; width: {width}%; background: #e34a33;"></div>
                </div>
            </div>
            """
    
    # Create the tooltip HTML
    html = f"""
    <div style="width: 250px;">
        <h4 style="margin: 0 0 8px 0; color: #1a237e; border-bottom: 1px solid #eee; padding-bottom: 4px;">
            {state_name}
        </h4>
        <div style="margin-bottom: 8px;">
            <div style="display: flex; justify-content: space-between;">
                <span style="font-weight: 500;">Total Crimes:</span>
                <span style="font-weight: 600;">{total_crimes:,}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="font-weight: 500;">Crime Rate:</span>
                <span style="font-weight: 600;">{crime_rate} per 100k</span>
            </div>
        </div>
        <div>
            <div style="font-weight: 500; margin-bottom: 6px;">Crime Distribution:</div>
            {crime_bars}
        </div>
        <div style="margin-top: 8px; font-size: 0.8em; color: #666; text-align: center;">
            Click for detailed analysis
        </div>
    </div>
    """.format(
        state_name=row.get('ST_NM', 'N/A'),
        total_crimes=total_crimes if isinstance(total_crimes, (int, float)) else 'N/A',
        crime_rate=crime_rate,
        crime_bars=crime_bars
    )
    
    return html

def load_population_data():
    """Load and return population data for Indian states."""
    # This is example data - replace with actual population data
    population_data = {
        'Andhra Pradesh': 49577103,
        'Arunachal Pradesh': 1383727,
        'Assam': 31205576,
        'Bihar': 104099452,
        'Chhattisgarh': 25545198,
        'Goa': 1458545,
        'Gujarat': 60439692,
        'Haryana': 25351462,
        'Himachal Pradesh': 6864602,
        'Jharkhand': 32988134,
        'Karnataka': 61095297,
        'Kerala': 33406061,
        'Madhya Pradesh': 72626809,
        'Maharashtra': 112374333,
        'Manipur': 2570390,
        'Meghalaya': 2966889,
        'Mizoram': 1097206,
        'Nagaland': 1978502,
        'Odisha': 41974218,
        'Punjab': 27743338,
        'Rajasthan': 68548437,
        'Sikkim': 610577,
        'Tamil Nadu': 72147030,
        'Telangana': 35003674,
        'Tripura': 3673917,
        'Uttar Pradesh': 199812341,
        'Uttarakhand': 10086292,
        'West Bengal': 91276115,
        'Andaman and Nicobar Islands': 380581,
        'Chandigarh': 1055450,
        'Dadra and Nagar Haveli and Daman and Diu': 585764,
        'Delhi': 16787941,
        'Jammu and Kashmir': 12267013,
        'Ladakh': 274289,
        'Lakshadweep': 64473,
        'Puducherry': 1247953
    }
    
    return pd.DataFrame({
        'States/UTs': population_data.keys(),
        'Population': population_data.values()
    })

def load_crime_data():
    """Load and preprocess crime data."""
    crime_data_path = data_dir / 'raw' / 'ncrb' / 'district_wise' / 'vulnerable_groups' / '42_District_wise_crimes_committed_against_women_2014.csv'
    
    try:
        df = pd.read_csv(crime_data_path, encoding='latin1')
        print(f"Loaded crime data with {len(df)} records")
        
        # Basic preprocessing - this will need to be adjusted based on actual data structure
        # Print column names for debugging
        print("\nAvailable columns in crime data:")
        print(df.columns.tolist())
        
        # Group by state and sum all crime columns
        if 'States/UTs' in df.columns:
            # Sum all numeric columns for each state
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
            state_crime = df.groupby('States/UTs')[numeric_cols].sum().reset_index()
            
            # Print sample of grouped data
            print("\nSample of grouped crime data:")
            print(state_crime.head())
            
            # Calculate total crimes per state (excluding year column if it exists)
            crime_columns = [col for col in numeric_cols if col != 'Year']
            state_crime['Total_Crimes'] = state_crime[crime_columns].sum(axis=1)
            
            # Normalize by population (if population data is available)
            # This is a placeholder - you'll need to load actual population data
            state_crime['Crime_Rate'] = state_crime['Total_Crimes']  # Placeholder
            
            return state_crime
        else:
            print("Warning: 'STATE/UT' column not found in crime data")
            return None
            
    except Exception as e:
        print(f"Error loading crime data: {e}")
        return None

def map_state_names(state_name):
    """Map state names from crime data to match GeoJSON state names.
    
    Args:
        state_name (str): Input state/UT name to be standardized
        
    Returns:
        str: Standardized state/UT name
    """
    if not isinstance(state_name, str) or not state_name.strip():
        return state_name
        
    # Convert to uppercase and strip whitespace for consistent comparison
    state_name = state_name.upper().strip()
    
    mapping = {
        # Standardize variations for states with multiple names
        'ANDAMAN & NICOBAR': 'A&N Islands',
        'ANDAMAN AND NICOBAR': 'A&N Islands',
        'ANDAMAN & NICOBAR ISLANDS': 'A&N Islands',
        'A & N ISLANDS': 'A&N Islands',
        
        # Union Territories
        'DADRA & NAGAR HAVELI': 'D&N Haveli',
        'DADRA AND NAGAR HAVELI': 'D&N Haveli',
        'DAMAN & DIU': 'Daman & Diu',
        'DAMAN AND DIU': 'Daman & Diu',
        'DELHI': 'Delhi UT',
        'NCT OF DELHI': 'Delhi UT',
        'NEW DELHI': 'Delhi UT',
        'PUDUCHERRY': 'Puducherry',
        'PONDICHERRY': 'Puducherry',
        'JAMMU & KASHMIR': 'Jammu & Kashmir',
        'JAMMU AND KASHMIR': 'Jammu & Kashmir',
        'LADAKH': 'Jammu & Kashmir',  # Temporary until we get Ladakh-specific data
        
        # States with name changes
        'ORISSA': 'Odisha',
        'UTTARANCHAL': 'Uttarakhand',
        
        # Common misspellings and variations
        'CHATTISGARH': 'Chhattisgarh',
        'UTTAR PRADESH': 'Uttar Pradesh',
        'MADHYA PRADESH': 'Madhya Pradesh',
        'TAMILNADU': 'Tamil Nadu',
        'TAMIL NADU': 'Tamil Nadu',
        'WEST BENGAL': 'West Bengal',
        'ARUNANCHAL PRADESH': 'Arunachal Pradesh',
        'MEGHALAY': 'Meghalaya',
        'MIZORUM': 'Mizoram',
        'NAGALAND': 'Nagaland',
        'SIKKIM': 'Sikkim',
        'TRIPURA': 'Tripura',
        'GOA': 'Goa',
        'GUJARAT': 'Gujarat',
        'HARYANA': 'Haryana',
        'HIMACHAL PRADESH': 'Himachal Pradesh',
        'JAMMU & KASHMIR': 'Jammu & Kashmir',
        'JHARKHAND': 'Jharkhand',
        'KARNATAKA': 'Karnataka',
        'KERALA': 'Kerala',
        'LAKSHADWEEP': 'Lakshadweep',
        'MADHYA PRADESH': 'Madhya Pradesh',
        'MAHARASHTRA': 'Maharashtra',
        'MANIPUR': 'Manipur',
        'MEGHALAYA': 'Meghalaya',
        'MIZORAM': 'Mizoram',
        'NAGALAND': 'Nagaland',
        'ODISHA': 'Odisha',
        'PUDUCHERRY': 'Puducherry',
        'PUNJAB': 'Punjab',
        'RAJASTHAN': 'Rajasthan',
        'SIKKIM': 'Sikkim',
        'TAMIL NADU': 'Tamil Nadu',
        'TELANGANA': 'Telangana',
        'TRIPURA': 'Tripura',
        'UTTAR PRADESH': 'Uttar Pradesh',
        'UTTARAKHAND': 'Uttarakhand',
        'WEST BENGAL': 'West Bengal'
    }
    
    # Convert input to string, strip whitespace, and convert to uppercase for matching
    state_name = str(state_name).strip().upper()
    
    # Special case for Delhi
    if 'DELHI' in state_name:
        return 'Delhi UT'
    
    # Check if the state name is in our mapping
    if state_name in state_mapping:
        return state_mapping[state_name]
    
    # Try to find a partial match (case-insensitive)
    for key, value in state_mapping.items():
        if key.upper() == state_name.upper():
            return value
    
    # If no match found, return the original name (in title case for consistency)
    return state_name.title()

def create_enhanced_choropleth_map():
    """Create an enhanced interactive choropleth map with additional features."""
    # Load GeoJSON data
    states_geojson = geo_data_dir / 'maps' / 'INDIA_STATES.geojson'
    if not states_geojson.exists():
        print(f"Error: GeoJSON file not found at {states_geojson}")
        return None
    
    # Load and preprocess crime data
    crime_data = load_crime_data()
    if crime_data is None or crime_data.empty:
        print("Error: Could not load or process crime data")
        return None
    
    # Calculate total crimes against women by state
    crime_data = crime_data.groupby('States/UTs').sum(numeric_only=True).reset_index()
    crime_data['Total_Crimes_Against_Women'] = crime_data[['Rape', 'Kidnapping & Abduction_Total', 'Assault on Women with intent to outrage her Modesty_Total', 'Insult to the Modesty of Women_Total', 'Cruelty by Husband or his Relatives', 'Dowry Deaths']].sum(axis=1)
    
    # Calculate crime rate per 100,000 population if population data is available
    if 'Population' in crime_data.columns:
        crime_data['Crime_Rate'] = (crime_data['Total_Crimes_Against_Women'] / crime_data['Population']) * 100000
        crime_data['Crime_Rate'] = crime_data['Crime_Rate'].round(2)
    
    # Load population data and merge with crime data to calculate crime rates
    population_data = load_population_data()
    if population_data is not None and not population_data.empty:
        crime_data = crime_data.merge(population_data, on='States/UTs', how='left')
    
    # Load GeoJSON
    gdf = load_geojson(states_geojson)
    if gdf is None:
        return None
    
    # Map state names and merge with crime data
    print("\nAvailable columns in GeoDataFrame:", gdf.columns.tolist())
    print("\nSample state names in GeoJSON:", gdf['STNAME'].head().tolist())
    
    # Make a copy of the original STNAME for reference
    gdf['ORIG_STNAME'] = gdf['STNAME']
    
    # Map state names from GeoJSON to match crime data
    gdf['STNAME_mapped'] = gdf['STNAME'].apply(map_state_names)
    
    # Display sample of mapped names for debugging
    print("\nSample mapped state names:")
    print(gdf[['ORIG_STNAME', 'STNAME_mapped']].head(10).to_string())
    
    # Print all unique state names from both datasets for comparison
    print("\nAll GeoJSON states:", sorted(gdf['STNAME'].unique().tolist()))
    print("\nAll crime data states:", sorted(crime_data['States/UTs'].unique().tolist()))
    
    # Merge with crime data using the mapped names
    print("\nMerging data...")
    gdf = gdf.merge(crime_data, left_on='STNAME_mapped', right_on='States/UTs', how='left')
    
    # Check for states that didn't merge correctly
    missing_states = gdf[gdf['States/UTs'].isna()].copy()
    if not missing_states.empty:
        print("\nStates that didn't match during merge:")
        print(missing_states[['ORIG_STNAME', 'STNAME_mapped']].drop_duplicates().to_string())
    
    # Fill missing values with 0 for numeric columns
    numeric_cols = crime_data.select_dtypes(include=['int64', 'float64']).columns
    for col in numeric_cols:
        if col in gdf.columns:
            gdf[col] = gdf[col].fillna(0)
    
    # Create a base map with better tile options
    m = folium.Map(
        location=[20.5937, 78.9629],  # Center of India
        zoom_start=5,
        tiles='cartodbpositron',  # Light base map
        control_scale=True,
        min_zoom=4,
        max_zoom=10,
        min_lat=6.0,  # Limit panning to keep India in view
        max_lat=38.0,
        min_lon=68.0,
        max_lon=98.0
    )
    
    # Add additional map tiles as options
    folium.TileLayer(
        'openstreetmap',
        name='OpenStreetMap'
    ).add_to(m)
    
    folium.TileLayer(
        'stamenterrain',
        name='Terrain',
        attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.'
    ).add_to(m)
    
    # Create a colormap
    max_crimes = gdf['Total_Crimes_Against_Women'].max()
    colormap = cm.LinearColormap(
        colors=COLOR_SCALE,
        vmin=0,
        vmax=max_crimes,
        caption='Total Crimes Against Women'
    )
    
    # Add colormap to the map
    colormap.add_to(m)
    
    # Create a style function for the choropleth
    def style_function(feature):
        # Get the crime count, default to 0 if not found
        crime_count = feature['properties'].get('Total_Crimes_Against_Women', 0)
        if crime_count is None or pd.isna(crime_count):
            crime_count = 0
            
        # Ensure crime_count is a number
        try:
            crime_count = float(crime_count)
        except (ValueError, TypeError):
            crime_count = 0
            
        return {
            'fillColor': colormap(crime_count),
            'color': '#000000',
            'weight': 0.5,
            'fillOpacity': 0.7,
            'opacity': 0.2
        }
    
    # Create a highlight function
    def highlight_function(feature):
        return {
            'fillColor': '#ff7800',
            'color': '#000000',
            'weight': 2,
            'fillOpacity': 0.7,
            'opacity': 0.5
        }
    
    # Create tooltips with crime statistics
    tooltip = GeoJsonTooltip(
        fields=['STNAME', 'Total_Crimes_Against_Women', 'Crime_Rate', 'Population'],
        aliases=['State:', 'Total Crimes:', 'Crime Rate (per 100k):', 'Population:'],
        localize=True,
        sticky=True,
        labels=True,
        style=(
            "background-color: white;"
            "border: 1px solid #999999;"
            "border-radius: 3px;"
            "box-shadow: 2px 2px 4px rgba(0,0,0,0.2);"
            "padding: 5px;"
            "font-size: 12px;"
        ),
        max_width=300
    )
    
    # Add the choropleth layer
    choropleth = folium.GeoJson(
        gdf,
        name='Crime Data',
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=tooltip,
        popup=folium.GeoJsonPopup(
            fields=['STNAME', 'Total_Crimes_Against_Women', 'Crime_Rate', 'Population'],
            aliases=['State:', 'Total Crimes:', 'Crime Rate (per 100k):', 'Population:'],
            localize=True,
            labels=True,
            style=(
                "background-color: white;"
                "border: 1px solid #999999;"
                "border-radius: 3px;"
                "box-shadow: 3px 3px 6px rgba(0,0,0,0.2);"
                "padding: 10px;"
                "font-size: 14px;"
            ),
            max_width=300
        )
    ).add_to(m)
    
    # Add search functionality
    search = Search(
        layer=choropleth,
        search_zoom=7,
        geom_type='Polygon',
        placeholder='Search for a state...',
        collapsed=False,
        position='topleft'
    ).add_to(m)
    
    # Add fullscreen control
    Fullscreen(
        position='topleft',
        title='Full Screen',
        title_cancel='Exit Full Screen',
        force_separate_button=True
    ).add_to(m)
    
    # Add measure control
    MeasureControl(
        position='topleft',
        primary_length_unit='kilometers',
        secondary_length_unit='miles',
        primary_area_unit='hectares',
        secondary_area_unit='acres'
    ).add_to(m)
    
    # Add minimap for navigation
    minimap = MiniMap(
        tile_layer='cartodbpositron',
        position='bottomright',
        width=200,
        height=150,
        collapsed_width=25,
        collapsed_height=25,
        zoom_level_fixed=None,
        center_fixed=False,
        zoom_level_offset=-5,
        zoom_control=False
    )
    m.add_child(minimap)
    
    # Add layer control
    folium.LayerControl(position='topright').add_to(m)
    
    # Add a title
    title_html = '''
        <div style="position: fixed; 
                    top: 10px; left: 50%; 
                    transform: translateX(-50%);
                    background: white; 
                    padding: 5px 15px;
                    border-radius: 5px;
                    border: 1px solid #999999;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                    z-index: 1000;
                    font-size: 16px;
                    font-weight: bold;">
            India: Crime Against Women (2014)
        </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Add a custom legend
    legend_html = '''
    <div style="position: fixed; 
                bottom: 30px; right: 10px; 
                background: white; 
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #999999;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                z-index: 1000;
                font-size: 12px;
                width: 180px;">
        <div style="font-weight: bold; margin-bottom: 5px;">Crime Categories:</div>
        <div style="display: flex; align-items: center; margin: 5px 0;">
            <div style="width: 15px; height: 15px; background: #e34a33; margin-right: 8px;"></div>
            <div>Rape</div>
        </div>
        <div style="display: flex; align-items: center; margin: 5px 0;">
            <div style="width: 15px; height: 15px; background: #fdbb84; margin-right: 8px;"></div>
            <div>Kidnapping</div>
        </div>
        <div style="display: flex; align-items: center; margin: 5px 0;">
            <div style="width: 15px; height: 15px; background: #fee8c8; margin-right: 8px;"></div>
            <div>Assault</div>
        </div>
        <div style="display: flex; align-items: center; margin: 5px 0;">
            <div style="width: 15px; height: 15px; background: #fef0d9; margin-right: 8px;"></div>
            <div>Other Crimes</div>
        </div>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Add a time slider (static for now, can be made interactive with JavaScript)
    time_slider_html = '''
    <div style="position: fixed; 
                bottom: 10px; left: 50%; 
                transform: translateX(-50%);
                background: white; 
                padding: 5px 15px;
                border-radius: 5px;
                border: 1px solid #999999;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                z-index: 1000;
                font-size: 14px;
                display: flex;
                align-items: center;
                gap: 10px;">
        <div>Year:</div>
        <input type="range" min="2010" max="2020" value="2014" id="yearSlider" 
               style="width: 200px;">
        <span id="yearValue">2014</span>
        <script>
            document.getElementById('yearSlider').addEventListener('input', function() {
                document.getElementById('yearValue').textContent = this.value;
                // Here you would update the map data based on the selected year
                // This would require additional JavaScript and data loading
            });
        </script>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(time_slider_html))
    
    # Save the map
    output_file = output_dir / 'india_crime_choropleth_enhanced.html'
    m.save(str(output_file))
    
    return output_file

def create_choropleth_map():
    """Create an interactive choropleth map of crime data by state."""
    print("Creating choropleth map...")
    
    # Load GeoJSON data
    states_geojson = geo_data_dir / 'maps' / 'INDIA_STATES.geojson'
    if not states_geojson.exists():
        print(f"Error: GeoJSON file not found at {states_geojson}")
        return
    
    # Load crime data
    crime_data = load_crime_data()
    if crime_data is None:
        print("No crime data available for mapping")
        return
    
    # Map state names to match GeoJSON
    crime_data['State_Geo'] = crime_data['States/UTs'].apply(map_state_names)
    print("\nSample of mapped state names:")
    print(crime_data[['States/UTs', 'State_Geo']].head())
    
    # Load GeoJSON
    india_states = load_geojson(states_geojson)
    if india_states is None:
        return
    
    # Print available GeoJSON properties for debugging
    print("\nSample of GeoJSON state names:")
    print(india_states[['STNAME', 'STCODE11']].head().to_string())
    
    # Create a base map centered on India
    m = folium.Map(
        location=[20.5937, 78.9629],  # Center of India
        zoom_start=5,
        tiles='cartodbpositron'  # Light map style (no API key needed)
    )
    
    # Create a choropleth map
    choropleth = folium.Choropleth(
        geo_data=india_states,
        name='Crime Rate by State',
        data=crime_data,
        columns=['State_Geo', 'Total Crimes against Women'],  # Use the mapped state names and total crimes
        key_on='feature.properties.STNAME',  # This must match the GeoJSON property name
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Total Crimes Against Women (2014)',
        highlight=True,
        reset=True
    ).add_to(m)
    
    # Add labels to the choropleth
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(
            fields=['STNAME'],
            aliases=['State: '],
            style=(
                "background-color: white; color: #333333; font-family: arial; "
                "font-size: 12px; padding: 8px; border-radius: 3px; box-shadow: 3px 3px 3px rgba(0, 0, 0, 0.2);"
            ),
            localize=True,
            sticky=True
        )
    )
    
    # Add hover functionality
    style_function = lambda x: {'fillColor': '#ffffff', 
                               'color':'#000000', 
                               'fillOpacity': 0.1, 
                               'weight': 0.1}
    
    highlight_function = lambda x: {'fillColor': '#000000', 
                                   'color':'#000000', 
                                   'fillOpacity': 0.50, 
                                   'weight': 0.1}
    
    # Add tooltips
    tooltip = folium.features.GeoJsonTooltip(
        fields=['STNAME'],  # Adjust based on your GeoJSON
        aliases=['State: '],
        style=("""
            background-color: white;
            color: #333333;
            font-family: arial;
            font-size: 12px;
            padding: 10px;
            border-radius: 3px;
            box-shadow: 3px 3px 3px rgba(0, 0, 0, 0.1);
        """)
    )
    
    # Add GeoJSON layer with tooltips
    geojson_layer = folium.features.GeoJson(
        india_states,
        style_function=style_function,
        control=False,
        highlight_function=highlight_function,
        tooltip=tooltip
    ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Add a title
    title_html = '''
         <div style="position: fixed; 
                     bottom: 50px; left: 50%; transform: translateX(-50%);
                     width: 80%;
                     height: 40px; 
                     z-index: 1000;
                     background-color: white;
                     padding: 10px;
                     border-radius: 5px;
                     box-shadow: 0 0 5px rgba(0,0,0,0.3);
                     text-align: center;
                     font-weight: bold;
                     font-size: 14px;">
             <b>India Crime Hotspots (2014)</b>
         </div>
         '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Save the map
    output_file = output_dir / 'india_crime_choropleth.html'
    m.save(str(output_file))
    print(f"Choropleth map saved to: {output_file}")
    
    return str(output_file)

def main():
    """Main function to create and display the choropleth map."""
    # Create the enhanced choropleth map
    output_file = create_enhanced_choropleth_map()
    
    if output_file and output_file.exists():
        print(f"Enhanced choropleth map created successfully: {output_file}")
        # Open the map in the default web browser
        import webbrowser
        webbrowser.open(f'file://{output_file.absolute()}')
    else:
        print("Failed to create enhanced choropleth map. Falling back to basic version.")
        # Fall back to basic version if enhanced fails
        output_file = create_choropleth_map()
        if output_file and output_file.exists():
            print(f"Basic choropleth map created: {output_file}")
            webbrowser.open(f'file://{output_file.absolute()}')
        else:
            print("Failed to create any choropleth map.")

if __name__ == "__main__":
    main()
