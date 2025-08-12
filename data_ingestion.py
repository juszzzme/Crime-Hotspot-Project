"""
Data Ingestion Module for Crime Hotspot Project
Handles reading data from various file formats (PDF, CSV, Excel, GeoJSON)
"""
import os
import pandas as pd
from typing import Union, Dict, List
import json
import zipfile

class DataIngestor:
    def __init__(self, base_path: str = 'data/raw'):
        """
        Initialize the DataIngestor with base path for data files
        
        Args:
            base_path (str): Base directory path for raw data
        """
        self.base_path = base_path
        self.supported_formats = ['.csv', '.xlsx', '.xls', '.pdf', '.geojson', '.zip', '.shp']
    
    def list_available_files(self) -> Dict[str, List[str]]:
        """List all available data files in the raw directory"""
        files = {}
        for root, _, filenames in os.walk(self.base_path):
            for filename in filenames:
                if any(filename.lower().endswith(ext) for ext in self.supported_formats):
                    rel_dir = os.path.relpath(root, self.base_path)
                    if rel_dir not in files:
                        files[rel_dir] = []
                    files[rel_dir].append(filename)
        return files
    
    def read_csv(self, file_path: str) -> pd.DataFrame:
        """Read data from CSV file"""
        return pd.read_csv(file_path)
    
    def read_excel(self, file_path: str) -> Dict[str, pd.DataFrame]:
        """Read data from Excel file, returns a dictionary of DataFrames (one per sheet)"""
        return pd.read_excel(file_path, sheet_name=None)
    
    def read_pdf(self, file_path: str) -> List[str]:
        """
        Read data from PDF file using tabula-py
        Note: tabula-py requires Java to be installed
        """
        try:
            import tabula
            # Read all pages
            return tabula.read_pdf(file_path, pages='all')
        except ImportError:
            print("tabula-py is required for PDF processing. Install with: pip install tabula-py")
            return []
    
    def read_geojson(self, file_path: str) -> dict:
        """Read GeoJSON file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def extract_zip(self, file_path: str, extract_to: str = None) -> List[str]:
        """
        Extract ZIP file and return list of extracted files
        
        Args:
            file_path: Path to the ZIP file
            extract_to: Directory to extract to (defaults to same directory as ZIP)
        """
        if extract_to is None:
            extract_to = os.path.dirname(file_path)
            
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
            return zip_ref.namelist()
    
    def load_data(self, relative_path: str):
        """
        Load data from file based on its extension
        
        Args:
            relative_path: Path relative to base_path
            
        Returns:
            Loaded data (DataFrame, dict, or list depending on file type)
        """
        file_path = os.path.join(self.base_path, relative_path)
        _, ext = os.path.splitext(file_path.lower())
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if ext == '.csv':
            return self.read_csv(file_path)
        elif ext in ['.xlsx', '.xls']:
            return self.read_excel(file_path)
        elif ext == '.pdf':
            return self.read_pdf(file_path)
        elif ext == '.geojson':
            return self.read_geojson(file_path)
        elif ext == '.zip':
            return self.extract_zip(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

def main():
    # Example usage
    ingestor = DataIngestor()
    
    # List available files
    print("Available data files:")
    files = ingestor.list_available_files()
    for directory, file_list in files.items():
        print(f"\n{directory}:")
        for file in file_list:
            print(f"  - {file}")
    
    # Example of loading a file (uncomment and modify as needed)
    # if 'ncrb' in files and files['ncrb']:
    #     print("\nProcessing NCRB file:", files['ncrb'][0])
    #     data = ingestor.load_data(os.path.join('ncrb', files['ncrb'][0]))
    #     print("Data shape/type:", data.shape if hasattr(data, 'shape') else type(data))

if __name__ == "__main__":
    main()
