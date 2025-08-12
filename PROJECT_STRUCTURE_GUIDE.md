# Crime Hotspot Project - Structure Guide

## Project Directory Structure

```
Crime-Hotspot-Project/
├── data/                           # All data files
│   ├── raw/                        # Original, unprocessed data
│   │   ├── ncrb/                   # NCRB (National Crime Records Bureau) data
│   │   │   ├── district_wise/      # District-wise crime data
│   │   │   └── state_wise/        # State-wise crime data
│   │   └── police/                # Data from state/city police departments
│   └── processed/                 # Processed and cleaned data
│       ├── cleaned_data/          # Cleaned data files
│       │   └── filtered_out/      # Data that was filtered out during processing
│       └── aggregated/            # Aggregated data for visualization
├── notebooks/                     # Jupyter notebooks for analysis
├── scripts/                       # Python scripts for data processing
│   ├── data_cleaning_tutorial.py  # Tutorial on data cleaning techniques
│   ├── filter_and_process_data.py # Script to filter and process data
│   ├── pdf_text_extraction.py     # Script to extract text from PDFs
│   └── explore_csv_data.py        # Script to explore CSV data
├── static/                        # Static files for web app (CSS, JS, images)
└── README.md                      # Project documentation
```

## Key Files and Their Purposes

### Data Files
- **Raw Data Files**:
  - `data/raw/ncrb/district_wise/`: Contains district-level crime data from NCRB
  - `data/raw/ncrb/state_wise/`: Contains state-level crime data from NCRB
  - `data/raw/police/`: Contains data from various state/city police departments

- **Processed Data Files**:
  - `data/processed/cleaned_data/`: Contains cleaned versions of the raw data
  - `data/processed/aggregated/`: Contains aggregated data ready for visualization

### Scripts
1. **Data Processing**
   - `data_cleaning_tutorial.py`: Comprehensive tutorial on data cleaning techniques
   - `filter_and_process_data.py`: Processes and filters crime data
   - `pdf_text_extraction.py`: Extracts text and tables from PDF reports
   - `explore_csv_data.py`: Explores and analyzes CSV data files

2. **Data Organization**
   - `organize_data.py`: Organizes raw data into appropriate directories
   - `organize_zip_contents.py`: Extracts and organizes ZIP file contents
   - `organize_district_data.py`: Organizes district-level crime data

### Output Files
- `data/processed/processing_summary.json`: Summary of data processing results
- `data/processed/cleaned_data/`: Contains all cleaned data files
- `data/processed/cleaned_data/filtered_out/`: Contains data that was filtered out during processing

## Data Processing Pipeline

1. **Data Collection**
   - Gather data from NCRB reports and police department sources
   - Organize data into appropriate directories

2. **Data Cleaning**
   - Handle missing values
   - Standardize column names and data formats
   - Remove duplicates and irrelevant data

3. **Data Transformation**
   - Aggregate data by location and time period
   - Calculate derived metrics (e.g., crime rates)
   - Merge related datasets

4. **Data Analysis**
   - Explore patterns and trends
   - Identify crime hotspots
   - Generate insights and visualizations

## Next Steps

1. **Data Analysis**: Use the cleaned data to analyze crime patterns
2. **Visualization**: Create interactive maps and charts
3. **Modeling**: Build predictive models for crime hotspots
4. **Web Application**: Develop a web interface for exploring the data

## Notes
- Always work with copies of the original data to preserve the raw data
- Document any data transformations or assumptions made during processing
- Keep the data processing pipeline reproducible by using scripts
- Regularly back up your data and code
