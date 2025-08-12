# Data Processing Techniques Guide

## Table of Contents
1. [Data Cleaning](#data-cleaning)
2. [Data Transformation](#data-transformation)
3. [Handling Missing Data](#handling-missing-data)
4. [Data Standardization](#data-standardization)
5. [Data Filtering](#data-filtering)
6. [File Processing](#file-processing)
7. [Best Practices](#best-practices)

---

## Data Cleaning

### 1. Handling Column Names
```python
def clean_column_names(df):
    """Standardize column names by converting to lowercase and replacing spaces with underscores."""
    df.columns = (df.columns
                 .str.lower()
                 .str.replace(' ', '_')
                 .str.replace('.', '')
                 .str.replace('-', '_')
                 .str.strip())
    return df
```
**Key Points:**
- Consistent naming conventions make code more maintainable
- Removes special characters that might cause issues in code
- Makes column names more Pythonic

### 2. Standardizing State Names
```python
def standardize_state_names(df, state_col='state'):
    """Standardize state/UT names to a consistent format."""
    state_mapping = {
        'DELHI (UT)': 'DELHI',
        'A&N ISLANDS': 'ANDAMAN & NICOBAR ISLANDS',
        'D&N HAVELI': 'DADRA & NAGAR HAVELI',
        'TAMILNADU': 'TAMIL NADU',
        'PONDICHERRY': 'PUDUCHERRY'
    }
    df[state_col] = df[state_col].str.upper().str.strip().replace(state_mapping)
    return df
```
**Key Points:**
- Ensures consistent state names across datasets
- Handles variations in naming conventions
- Makes merging datasets more reliable

## Data Transformation

### 1. Converting Data Types
```python
def convert_to_numeric(df, columns=None):
    """Convert specified columns to numeric, coercing errors to NaN."""
    if columns is None:
        columns = df.select_dtypes(include=['object']).columns
    
    for col in columns:
        try:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        except Exception as e:
            print(f"Could not convert {col}: {e}")
    return df
```
**Key Points:**
- Ensures numeric operations can be performed on numerical data
- Handles conversion errors gracefully
- Use `errors='coerce'` to convert non-numeric values to NaN

## Handling Missing Data

### 1. Filling Missing Values
```python
def fill_missing_values(df, strategy=0, columns=None):
    """
    Fill missing values using the specified strategy.
    
    Args:
        df: Input DataFrame
        strategy: 'mean', 'median', 'mode', or a specific value
        columns: List of columns to process (None for all columns)
    """
    if columns is None:
        columns = df.columns
    
    for col in columns:
        if df[col].isnull().any():
            if strategy == 'mean':
                df[col].fillna(df[col].mean(), inplace=True)
            elif strategy == 'median':
                df[col].fillna(df[col].median(), inplace=True)
            elif strategy == 'mode':
                df[col].fillna(df[col].mode()[0], inplace=True)
            else:
                df[col].fillna(strategy, inplace=True)
    return df
```
**Key Points:**
- Choose filling strategy based on data characteristics
- For numerical data: mean, median, or mode
- For categorical data: mode or a specific value (e.g., 'Unknown')

## Data Standardization

### 1. Standardizing Date Formats
```python
def standardize_dates(df, date_columns):
    """Convert date columns to datetime format."""
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df
```
**Key Points:**
- Ensures consistent date formats
- Handles various date string formats
- Converts to datetime objects for time-based operations

## Data Filtering

### 1. Filtering by State
```python
def filter_by_states(df, states_to_keep, state_col='state'):
    """Filter DataFrame to include only specified states."""
    if state_col not in df.columns:
        return df, pd.DataFrame()
    
    mask = df[state_col].str.upper().isin([s.upper() for s in states_to_keep])
    return df[mask].copy(), df[~mask].copy()
```
**Key Points:**
- Case-insensitive comparison
- Returns both matching and non-matching rows
- Preserves original data by returning a copy

## File Processing

### 1. Processing Multiple Files
```python
def process_directory(input_dir, output_dir, file_processor):
    """Process all files in a directory using the provided processor function."""
    os.makedirs(output_dir, exist_ok=True)
    results = []
    
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.csv'):
                input_path = os.path.join(root, file)
                output_path = os.path.join(output_dir, f"processed_{file}")
                
                try:
                    result = file_processor(input_path, output_path)
                    results.append({
                        'file': file,
                        'status': 'success',
                        'result': result
                    })
                except Exception as e:
                    results.append({
                        'file': file,
                        'status': 'error',
                        'error': str(e)
                    })
    
    return results
```
**Key Points:**
- Processes all files in a directory recursively
- Handles errors for individual files
- Returns processing results for each file

## Best Practices

1. **Data Validation**
   - Check for duplicate rows
   - Validate data ranges (e.g., negative values for counts)
   - Verify relationships between columns

2. **Performance Tips**
   - Use vectorized operations instead of loops
   - Process data in chunks for large files
   - Use appropriate data types to reduce memory usage

3. **Reproducibility**
   - Set random seeds for any random operations
   - Document all data transformations
   - Save processing logs

4. **Error Handling**
   - Use try-except blocks for file operations
   - Log errors with sufficient context
   - Continue processing other files if one fails

5. **Documentation**
   - Document data sources and processing steps
   - Include examples of input and output data
   - Note any assumptions or limitations

## Common Pitfalls

1. **Memory Issues**
   - Loading large files into memory
   - Creating too many intermediate DataFrames
   - Not using chunking for large datasets

2. **Data Quality**
   - Not checking for duplicate or missing values
   - Ignoring data type mismatches
   - Not validating data ranges

3. **Performance**
   - Using Python loops instead of vectorized operations
   - Not using efficient data structures
   - Reading the same file multiple times

## Next Steps

1. **Data Analysis**
   - Calculate summary statistics
   - Identify trends and patterns
   - Create visualizations

2. **Feature Engineering**
   - Create derived features
   - Normalize or scale features
   - Handle categorical variables

3. **Model Building**
   - Split data into training and test sets
   - Train machine learning models
   - Evaluate model performance

4. **Deployment**
   - Create a web interface
   - Set up automated data pipelines
   - Monitor data quality over time
