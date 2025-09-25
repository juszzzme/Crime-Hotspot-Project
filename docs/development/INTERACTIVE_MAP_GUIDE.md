# Interactive Map Guide

This document provides information about the interactive map component of the Crime Hotspot Project.

## Overview

The interactive map visualizes crime data across Indian states using open-source mapping libraries. It's designed to work without requiring any paid API keys.

## Features

- **State Boundaries**: Displays all Indian states with hover information
- **Responsive Design**: Works on both desktop and mobile devices
- **No API Key Required**: Uses open-source tile layers
- **Custom Styling**: Clean, professional appearance

## How to Use

1. The map is generated as an HTML file located at:
   ```
   reports/maps/india_crime_map.html
   ```

2. Open the file in any modern web browser to view the interactive map.

3. Interact with the map:
   - Hover over states to see their names
   - Use the mouse wheel to zoom in/out
   - Click and drag to pan around the map
   - Use the layer control (top-right) to toggle layers (if available)

## Technical Details

### Dependencies

- Python 3.7+
- folium
- geopandas
- pandas

### Data Sources

- State boundaries: `data/raw/geographic/maps/INDIA_STATES.geojson`
- Crime data: `data/raw/ncrb/district_wise/vulnerable_groups/`

### Customization

To modify the map's appearance or behavior, edit:
```
src/visualization/interactive_map.py
```

Key parameters you might want to adjust:
- Map center coordinates
- Initial zoom level
- Color schemes
- Tooltip styling

## Future Enhancements

- Add crime data visualization layers
- Implement choropleth mapping for crime rates
- Add district-level boundaries
- Include time-series visualization
- Add search functionality

## Troubleshooting

If the map doesn't display properly:
1. Ensure all dependencies are installed
2. Verify that the GeoJSON file exists at the expected location
3. Check the browser's developer console for JavaScript errors
4. Try opening the HTML file in a different web browser
