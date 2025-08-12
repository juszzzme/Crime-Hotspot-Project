import pdfplumber
import os
from pathlib import Path

def extract_text_from_pdf(pdf_path, output_dir="data/processed/ncrb_text"):
    """
    Extract text from a PDF and save it to a text file.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_dir (str): Directory to save extracted text
    """
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Create output file path
    pdf_name = Path(pdf_path).stem
    output_file = output_path / f"{pdf_name}_extracted.txt"
    
    print(f"Extracting text from {pdf_path}...")
    
    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        # Extract text from each page
        with open(output_file, 'w', encoding='utf-8') as f:
            for i, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    f.write(f"--- Page {i} ---\n")
                    f.write(text)
                    f.write("\n\n")
    
    print(f"Text extracted and saved to {output_file}")
    return output_file

def extract_tables_from_pdf(pdf_path, output_dir="data/processed/ncrb_tables"):
    """
    Extract tables from a PDF using pdfplumber and save them as CSV files.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_dir (str): Directory to save extracted tables
    """
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"Extracting tables from {pdf_path}...")
    
    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            # Extract tables from the page
            tables = page.extract_tables()
            
            # Save each table as a CSV file
            for j, table in enumerate(tables, 1):
                if table:  # Only process non-empty tables
                    # Convert to DataFrame for easier handling
                    import pandas as pd
                    df = pd.DataFrame(table[1:], columns=table[0])
                    
                    # Save to CSV
                    output_file = output_path / f"table_page{i}_{j}.csv"
                    df.to_csv(output_file, index=False)
                    print(f"Saved table from page {i} as {output_file}")
    
    print("Table extraction complete!")

if __name__ == "__main__":
    # Path to the NCRB PDF
    pdf_path = "data/raw/ncrb/crimeinIndia2022Book1.pdf"
    
    # Check if the file exists
    if not os.path.exists(pdf_path):
        print(f"Error: File not found at {pdf_path}")
        print("Please make sure the file exists and the path is correct.")
    else:
        # Extract text from the PDF
        text_file = extract_text_from_pdf(pdf_path)
        print(f"\nExtracted text saved to: {text_file}")
        
        # Extract tables from the PDF
        print("\nExtracting tables...")
        extract_tables_from_pdf(pdf_path)
        
        print("\nDone! Check the 'data/processed/' directory for extracted content.")
