# Crime Hotspot Visualization Project

An interactive visualization tool for analyzing crime patterns across India, with a focus on Tamil Nadu and Chennai.

## Features

- **Interactive Maps**: Visualize crime data across Indian states
- **Data Analysis**: Explore crime trends and patterns
- **Open Source**: No paid APIs required
- **Local Data**: Works with locally stored data files

## Getting Started

### Prerequisites

- Python 3.7+
- Anaconda (recommended)
- Required Python packages (install using `pip install -r requirements.txt`):
  - pandas
  - geopandas
  - folium
  - matplotlib
  - jupyter

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Crime-Hotspot-Project.git
   cd Crime-Hotspot-Project
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
├── data/                    # Data files
│   ├── raw/                # Original, immutable data
│   ├── processed/          # Cleaned and processed data
│   └── interim/            # Intermediate data
├── docs/                   # Documentation
├── notebooks/              # Jupyter notebooks for exploration
├── reports/                # Generated analysis and visualizations
│   ├── figures/            # Static visualizations
│   └── maps/               # Interactive map files
└── src/                    # Source code
    ├── data/               # Data processing scripts
    └── visualization/      # Visualization scripts
```

## Usage

### Generating the Interactive Map

1. Run the map generation script:
   ```bash
   python src/visualization/interactive_map.py
   ```

2. Open the generated HTML file in your browser:
   ```
   reports/maps/india_crime_map.html
   ```

### Exploring Data

Use the Jupyter notebooks in the `notebooks/` directory to explore the data:

```bash
jupyter notebook notebooks/exploratory/explore_geo_data.ipynb
```

## Documentation

- [Interactive Map Guide](docs/INTERACTIVE_MAP_GUIDE.md): How to use and customize the interactive map
- [Project Structure](docs/PROJECT_STRUCTURE_GUIDE.md): Detailed explanation of the project organization
- [Data Processing](docs/DATA_PROCESSING_TECHNIQUES.md): Information about data cleaning and processing

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Data sources: NCRB, OpenStreetMap
- Built with Python and open-source libraries
- Special thanks to all contributors
