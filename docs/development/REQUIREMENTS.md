# Project Requirements Checklist

*Last Updated: August 12, 2025*

## Data Requirements

### Crime Data
- [x] NCRB crime data (2012-2014) - Already have
- [ ] More recent NCRB data (2015-2023)
- [ ] City/neighborhood level crime data for major Indian cities
- [ ] Time series data for crime trends

### Geographic Data
- [ ] Shapefiles or GeoJSON for Indian states and districts
- [ ] City boundaries for major Indian cities
- [ ] Landmark data (police stations, hospitals, etc.)
- [ ] Population density data

### Places Implementation Data (Priority)
- [ ] **Hospital Locations**: Comprehensive database of hospitals with coordinates
  - [ ] Government hospitals
  - [ ] Private hospitals
  - [ ] Specialty medical centers
  - [ ] Emergency care facilities
- [ ] **Police Station Locations**: Complete police infrastructure data
  - [ ] Local police stations
  - [ ] Traffic police stations
  - [ ] Special branch offices
  - [ ] Police headquarters
- [ ] **Fire Station Locations**: Fire safety infrastructure
  - [ ] Fire stations with coordinates
  - [ ] Emergency response centers
  - [ ] Fire safety equipment locations
- [ ] **Educational Institutions**: Schools and colleges
  - [ ] Government schools
  - [ ] Private schools
  - [ ] Colleges and universities
  - [ ] Technical institutes
- [ ] **Public Facilities**: Essential civic infrastructure
  - [ ] Government offices
  - [ ] Post offices
  - [ ] Banks and ATMs
  - [ ] Public transportation hubs
- [ ] **Religious Places**: Temples, mosques, churches
  - [ ] Major temples
  - [ ] Mosques
  - [ ] Churches
  - [ ] Other religious sites
- [ ] **Commercial Areas**: Shopping and business districts
  - [ ] Shopping malls
  - [ ] Markets
  - [ ] Business districts
  - [ ] Commercial complexes

### Additional Datasets
- [ ] Socio-economic data (literacy rate, income levels)
- [ ] Police station locations and jurisdictions
- [ ] Public transportation routes and stops
- [ ] Nightlife and commercial area data

## Map Coordinates Needed

### For Chennai (Priority)
- [ ] Latitude/Longitude for police station locations
- [ ] Boundary coordinates for neighborhoods
- [ ] Hotspot areas with crime concentration

### For Other Major Cities
- [ ] Delhi/NCR
- [ ] Mumbai
- [ ] Bangalore
- [ ] Kolkata
- [ ] Hyderabad

## Technical Requirements

### APIs
- [ ] Google Maps API key (or alternative like Mapbox)
- [ ] Weather data API (if correlating with crime)

### Software
- [ ] QGIS or similar GIS software (for processing geographic data)
- [ ] Python environment with required libraries

## Places Implementation Strategy

### Data Sources for Places
- [ ] **Google Places API**: For comprehensive place data
  - [ ] Hospitals and medical facilities
  - [ ] Police stations and government offices
  - [ ] Schools and educational institutions
  - [ ] Shopping centers and malls
- [ ] **OpenStreetMap (OSM)**: Free alternative data source
  - [ ] Extract amenity data for hospitals, police, schools
  - [ ] Use Overpass API for querying OSM data
  - [ ] Process OSM data for Indian cities
- [ ] **Government Databases**: Official data sources
  - [ ] Ministry of Health hospital directory
  - [ ] Police department official locations
  - [ ] Education ministry school database
- [ ] **Manual Data Collection**: For missing or incomplete data
  - [ ] Verify coordinates for critical facilities
  - [ ] Add missing places through field research
  - [ ] Cross-reference multiple sources for accuracy

### Implementation Approach
- [ ] **Phase 1**: Start with Chennai city (current focus)
  - [ ] Implement hospital markers first (highest priority)
  - [ ] Add police station markers
  - [ ] Include fire stations and schools
- [ ] **Phase 2**: Expand to Tamil Nadu state
  - [ ] Major cities: Coimbatore, Madurai, Trichy
  - [ ] Use same marker system as Chennai
- [ ] **Phase 3**: Scale to other Indian states
  - [ ] Delhi, Mumbai, Bangalore, Kolkata
  - [ ] Maintain consistent marker design

### Technical Implementation
- [ ] **Marker System**: Use authentic Leaflet circle markers
  - [ ] Red markers for hospitals (medical cross-like)
  - [ ] Blue markers for police stations
  - [ ] Orange markers for fire stations
  - [ ] Green markers for schools
- [ ] **Data Storage**: Efficient data management
  - [ ] JSON files for place coordinates
  - [ ] Database integration for large datasets
  - [ ] Caching for performance optimization
- [ ] **User Interface**: Interactive place filtering
  - [ ] Category-based filtering (hospitals, police, etc.)
  - [ ] Distance-based search
  - [ ] Real-time marker updates

## Current Status
- Project structure has been reorganized
- Basic visualizations have been created
- Next step: Update file paths in scripts

---
*This document will be updated as the project progresses. Please check back regularly for updates.*
