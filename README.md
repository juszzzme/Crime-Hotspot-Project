# Crime Hotspot Visualization Platform

## Project Overview
An interactive web platform that visualizes crime hotspots across Indian cities with an AI-powered chatbot assistant. The platform allows users to explore crime data through zoomable maps and get real-time safety information.

## Features
- Interactive map with zoomable interface (Country → State → City → Neighborhood)
- Heatmap visualization of crime data
- AI Chatbot for crime-related queries
- Real-time crime statistics and safety tips
- Responsive design for all devices

## Project Structure
```
├── app.py                # Main Flask application
├── requirements.txt      # Python dependencies
├── data/                 # Data storage
│   ├── raw/             # Original, unprocessed data
│   └── processed/       # Cleaned and processed data
├── models/              # Trained ML models
├── static/              # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
└── templates/           # HTML templates
    └── index.html
```

## Setup Instructions
1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Place your data files in the appropriate directories
4. Run the application:
   ```
   python app.py
   ```
5. Open `http://localhost:5000` in your browser

## Data Requirements
Please organize your data in the following structure:
- `data/raw/ncrb/` - NCRB crime data (PDF)
- `data/raw/police/` - State/City police data (CSV/Excel)
- `data/raw/geo/` - Geographic data (shapefiles, GeoJSON)

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
