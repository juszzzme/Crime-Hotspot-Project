# Crime Data Analysis Report

*Last Updated: August 12, 2025*

## Overview
This document provides an overview of the preprocessed crime data, focusing on the key columns and their significance in our analysis.

## Data Sources
1. **NCRB (National Crime Records Bureau) Reports** (2012-2014)
2. **State Police Department CSVs**
3. **District-wise Crime Reports**

## Key Datasets and Their Structure

### 1. District-wise Crimes Against Women (2014)
**File**: `42_District_wise_crimes_committed_against_women_2014.csv`

| Column | Description | Data Type | Focus Area |
|--------|-------------|-----------|------------|
| district | Name of the district | String | Primary |
| year | Year of data (2014) | Integer | Primary |
| rape | Number of rape cases reported | Integer | High |
| murder | Number of murder cases reported | Integer | High |
| robbery | Number of robbery cases reported | Integer | Medium |
| arson | Number of arson cases reported | Integer | Medium |

**Focus Areas**: 
- Identifying districts with highest crime rates
- Analyzing correlation between different crime types
- Year-over-year comparison of crime statistics

### 2. Crime by Place of Occurrence (2001-2014)
**File**: `17_Crime_by_place_of_occurrence_*.csv`

| Column | Description | Data Type | Focus Area |
|--------|-------------|-----------|------------|
| place_type | Type of location where crime occurred | String | Primary |
| year | Year of data | Integer | Primary |
| count | Number of incidents | Integer | High |

### 3. Persons Arrested and Their Disposal (2012-2014)
**Files**: 
- `03_Persons_arrested_*.csv`
- `04_01_Person_arrested_*.csv` (SLL crimes)
- `04_02_Person_arrested_*.csv` (IPC crimes)

| Column | Description | Data Type | Focus Area |
|--------|-------------|-----------|------------|
| crime_type | Type of crime | String | Primary |
| state | State where crime occurred | String | High |
| district | District where crime occurred | String | High |
| year | Year of data | Integer | Primary |
| cases_reported | Number of cases reported | Integer | High |
| cases_convicted | Number of convictions | Integer | Medium |

## Data Quality Notes
- Some district names may have variations (e.g., "New Delhi" vs "New Delhi District")
- Data completeness varies by year and region
- Some fields may contain missing values (coded as NaN or empty strings)

## Next Steps in Analysis
1. **Data Enrichment**: Add geographic coordinates for mapping
2. **Time Series Analysis**: Track crime trends over the years
3. **Comparative Analysis**: Compare crime rates across different regions
4. **Predictive Modeling**: Develop models to predict crime hotspots

---
*This report will be updated as the analysis progresses.*
