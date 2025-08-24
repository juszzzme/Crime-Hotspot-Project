from datetime import datetime
from flask import Blueprint, render_template, request, current_app, abort, redirect, url_for, send_from_directory, jsonify
from flask_login import login_required, current_user, login_user
from app.models.user import User
import os
import json

bp = Blueprint('main', __name__)

@bp.route('/test-login')
def test_login():
    """Test route to automatically log in as admin for development purposes."""
    user = User.query.filter_by(username='admin').first()
    if user:
        login_user(user)
        return redirect(url_for('main.map'))
    return 'No admin user found'

@bp.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@bp.route('/')
def index():
    """Home page route."""
    return render_template('index.html')

@bp.route('/map')
@login_required
def map():
    """Interactive map view showing all of India."""
    return render_template('map.html', view_type='country', location_id='india')

@bp.route('/map/state/<state_name>')
@login_required
def state_map_view(state_name):
    """Interactive map view for a specific state."""
    # Normalize state name for file lookup
    state_name_normalized = state_name.lower().replace(' ', '-')
    
    # Check if state exists
    state_file_path = os.path.join(current_app.root_path, '..', 'Maps', 'States', f"{state_name_normalized}.geojson")
    if not os.path.exists(state_file_path):
        # Try alternate location
        state_file_path = os.path.join(current_app.root_path, '..', 'Maps', 'States', state_name_normalized, f"{state_name_normalized}.geojson")
        if not os.path.exists(state_file_path):
            current_app.logger.error(f"State file not found: {state_file_path}")
            abort(404)
    
    return render_template('map.html', view_type='state', location_id=state_name_normalized, location_name=state_name)

@bp.route('/map/city/<state_name>/<city_name>')
@login_required
def city_map_view(state_name, city_name):
    """Interactive map view for a specific city."""
    try:
        # Normalize names for file lookup
        state_name_normalized = state_name.lower().replace(' ', '-')
        city_name_normalized = city_name.lower().replace(' ', '-')
        
        # List of possible directory name formats to check
        possible_dir_names = [
            city_name_normalized.title(),  # Title case (Chennai)
            city_name_normalized.upper(),  # Uppercase (CHENNAI)
            city_name_normalized,          # Lowercase (chennai)
            city_name_normalized.replace('-', ' ').title().replace(' ', '')  # Remove hyphens and title case
        ]
        
        city_dir_path = None
        # Check each possible directory name format
        for dir_name in possible_dir_names:
            test_path = os.path.join(current_app.root_path, '..', 'Maps', 'Cities', dir_name)
            if os.path.exists(test_path):
                city_dir_path = test_path
                current_app.logger.info(f"Found city directory: {city_dir_path}")
                break
        
        if not city_dir_path:
            current_app.logger.error(f"City directory not found for: {city_name}")
            abort(404, description=f"City directory not found: {city_name}")

        # Look for GeoJSON file with various naming conventions
        possible_files = [
            f"{city_name_normalized}.geojson",
            f"{city_name_normalized.title()}.geojson",
            f"{city_name_normalized.upper()}.geojson",
            f"{city_name_normalized}1.geojson",
            f"{city_name_normalized.upper()}1.geojson",
            # Add more possible filenames if needed
            f"{os.path.basename(city_dir_path)}.geojson",
            f"{os.path.basename(city_dir_path).upper()}.geojson"
        ]
        
        # Also check for any .geojson file in the directory
        try:
            all_files = os.listdir(city_dir_path)
            geojson_files = [f for f in all_files if f.lower().endswith('.geojson')]
            if geojson_files:
                possible_files.extend(geojson_files)
        except Exception as e:
            current_app.logger.warning(f"Error listing directory contents: {str(e)}")

        # Look for the first existing GeoJSON file
        city_file_path = None
        for filename in possible_files:
            test_path = os.path.join(city_dir_path, filename)
            if os.path.exists(test_path):
                city_file_path = test_path
                current_app.logger.info(f"Found GeoJSON file: {city_file_path}")
                break

        if not city_file_path and geojson_files:
            # If we found geojson files but couldn't match them, use the first one
            city_file_path = os.path.join(city_dir_path, geojson_files[0])
            current_app.logger.info(f"Using first available GeoJSON file: {city_file_path}")

        if not city_file_path:
            current_app.logger.error(f"No GeoJSON file found in: {city_dir_path}")
            # Continue without GeoJSON file but log the issue
            current_app.logger.info(f"Continuing without GeoJSON for {city_name}")

        return render_template('map.html', 
                            view_type='city', 
                            location_id=city_name_normalized,
                            state_name=state_name, 
                            location_name=city_name)
                            
    except Exception as e:
        current_app.logger.error(f"Error loading city map for {city_name}: {str(e)}")
        current_app.logger.exception("Full traceback:")
        abort(500, description=f"Error loading city map: {str(e)}")

@bp.route('/ai-predictions')
@login_required
def ai_predictions():
    """AI-Powered Crime Predictions dashboard."""
    return render_template('ai_predictions.html')

@bp.route('/advanced-map')
@login_required
def advanced_map():
    """Advanced AI-powered crime map with enhanced features."""
    return render_template('advanced_map.html')

@bp.route('/pattern-analysis')
@login_required
def pattern_analysis():
    """Advanced AI crime pattern analysis dashboard."""
    return render_template('pattern_analysis.html')

@bp.route('/api/pattern-analysis')
@login_required
def pattern_analysis_api():
    """API endpoint for simple crime pattern analysis."""
    try:
        # Simple mock analysis data that always works
        analysis_results = {
            'success': True,
            'data': {
                'spatial_clusters': [
                    {'location': 'T. Nagar', 'incidents': 15, 'density': 'High'},
                    {'location': 'Anna Nagar', 'incidents': 12, 'density': 'Medium'},
                    {'location': 'Adyar', 'incidents': 8, 'density': 'Low'}
                ],
                'temporal_patterns': {
                    'peak_hours': '8-10 PM',
                    'peak_days': 'Friday-Saturday',
                    'trend': 'Increasing'
                },
                'anomaly_detection': [
                    {'type': 'Unusual spike', 'location': 'T. Nagar', 'severity': 'Medium'},
                    {'type': 'Pattern change', 'location': 'Velachery', 'severity': 'Low'}
                ],
                'risk_assessment': {
                    'overall_risk': 7.2,
                    'high_risk_areas': ['T. Nagar', 'Anna Nagar'],
                    'trend': 'Increasing'
                }
            },
            'metadata': {
                'analysis_timestamp': datetime.now().isoformat(),
                'data_points_analyzed': 247,
                'analysis_version': '1.0'
            }
        }

        return jsonify(analysis_results)

    except Exception as e:
        current_app.logger.error(f"Error in pattern analysis API: {str(e)}")

        return jsonify({
            'success': False,
            'error': 'Failed to analyze crime patterns. Please try again later.'
        }), 500

def generate_sample_crime_data():
    """Generate sample crime data for pattern analysis."""
    import random
    from datetime import datetime, timedelta

    crime_types = ['murder', 'rape', 'robbery', 'assault', 'burglary', 'theft', 'vandalism', 'drug']
    locations = ['T. Nagar', 'Anna Nagar', 'Adyar', 'Velachery', 'Tambaram', 'Chrompet', 'Porur']

    sample_data = []
    base_date = datetime.now() - timedelta(days=30)

    def is_on_land(lat, lng):
        """Check if coordinates are on land (not in ocean/water bodies)"""
        # Chennai land boundary validation
        chennai_land_bounds = {
            'north': 13.2,
            'south': 12.9,
            'east': 80.35,   # Reduced to exclude ocean
            'west': 80.1
        }

        # Check if coordinates are within basic bounds
        if (lat < chennai_land_bounds['south'] or lat > chennai_land_bounds['north'] or
            lng < chennai_land_bounds['west'] or lng > chennai_land_bounds['east']):
            return False

        # Exclude specific ocean/water areas
        water_areas = [
            # Bay of Bengal (eastern coast)
            {'min_lat': 12.9, 'max_lat': 13.2, 'min_lng': 80.25, 'max_lng': 80.35},
            # Adyar River mouth area
            {'min_lat': 13.0, 'max_lat': 13.05, 'min_lng': 80.24, 'max_lng': 80.28},
            # Cooum River mouth area
            {'min_lat': 13.08, 'max_lat': 13.09, 'min_lng': 80.28, 'max_lng': 80.32}
        ]

        # Check if point is in any water area
        for area in water_areas:
            if (lat >= area['min_lat'] and lat <= area['max_lat'] and
                lng >= area['min_lng'] and lng <= area['max_lng']):
                return False

        return True

    for i in range(200):  # Generate 200 sample incidents
        # Generate random coordinates around Chennai with land validation
        base_lat, base_lng = 13.0827, 80.2707
        attempts = 0
        while attempts < 10:
            lat = base_lat + random.uniform(-0.2, 0.2)
            lng = base_lng + random.uniform(-0.2, 0.2)
            if is_on_land(lat, lng):
                break
            attempts += 1

        # If we couldn't find a land coordinate after 10 attempts, use a known land location
        if attempts >= 10:
            land_locations = [
                (13.0827, 80.2707),  # T. Nagar
                (13.0569, 80.2425),  # Adyar
                (13.1185, 80.2574),  # Anna Nagar
                (13.0067, 80.2206),  # Velachery
                (13.0878, 80.2785)   # Mylapore
            ]
            random_land_location = random.choice(land_locations)
            lat = random_land_location[0] + random.uniform(-0.01, 0.01)  # Small variation
            lng = random_land_location[1] + random.uniform(-0.01, 0.01)

        # Generate random date within last 30 days
        random_days = random.randint(0, 30)
        incident_date = base_date + timedelta(days=random_days)

        # Generate time with some patterns (more crimes at night)
        hour_weights = [1, 1, 1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 6, 5, 4, 3, 4, 5, 6, 8, 9, 8, 6, 4]
        hour = random.choices(range(24), weights=hour_weights)[0]

        sample_data.append({
            'id': f'incident_{i}',
            'crime_type': random.choice(crime_types),
            'latitude': lat,
            'longitude': lng,
            'location': random.choice(locations),
            'date': incident_date.strftime('%Y-%m-%d'),
            'time': f'{hour:02d}:{random.randint(0, 59):02d}'
        })
    
    return sample_data

@bp.route('/geojson/cities/<city_name>')
def serve_city_geojson(city_name):
    """Serve GeoJSON files for cities with flexible path resolution."""
    try:
        # Normalize city name for directory lookup
        city_name = city_name.lower().replace(' ', '-')
        
        # Define possible base directories
        base_dir = os.path.join(current_app.root_path, '..', 'Maps', 'Cities')
        
        # Try different directory name formats
        possible_dirs = [
            city_name.title(),  # Title case (Chennai)
            city_name.upper(),  # Uppercase (CHENNAI)
            city_name,          # Lowercase (chennai)
            city_name.replace('-', ' ').title().replace(' ', '')  # Remove hyphens and title case
        ]
        
        # Look for the city directory
        city_dir = None
        for dir_name in possible_dirs:
            test_path = os.path.join(base_dir, dir_name)
            if os.path.isdir(test_path):
                city_dir = test_path
                break
        
        if not city_dir:
            current_app.logger.error(f"City directory not found for: {city_name}")
            abort(404, description=f"City directory not found: {city_name}")
        
        # Look for any GeoJSON file in the city directory
        geojson_file = None
        for file in os.listdir(city_dir):
            if file.lower().endswith('.geojson'):
                geojson_file = os.path.join(city_dir, file)
                break
        
        if not geojson_file:
            current_app.logger.error(f"No GeoJSON file found in directory: {city_dir}")
            abort(404, description=f"No GeoJSON file found for city: {city_name}")
        
        # Read and return the GeoJSON file
        with open(geojson_file, 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)
        
        return jsonify(geojson_data)
        
    except Exception as e:
        current_app.logger.error(f"Error serving city GeoJSON for {city_name}: {str(e)}")
        current_app.logger.exception("Full traceback:")
        abort(500, description=f"Error loading city data: {str(e)}")

@bp.route('/static/geojson/<path:filename>')
def serve_geojson(filename):
    """Serve GeoJSON files from the Maps directory."""
    try:
        # Get the project root directory (parent of app directory)
        project_root = os.path.dirname(current_app.root_path)
        maps_dir = os.path.join(project_root, 'Maps')

        # Handle different file paths
        if filename == 'india.geojson':
            # Main India GeoJSON file
            file_path = os.path.join(maps_dir, 'india.geojson')
        elif filename.startswith('states/'):
            # State-specific GeoJSON files
            state_file = filename.replace('states/', '')
            file_path = os.path.join(maps_dir, 'States', state_file)
        elif filename.startswith('cities/'):
            # City-specific GeoJSON files
            city_file = filename.replace('cities/', '')
            # Extract city name from path (e.g., 'mumbai/mumbai.geojson' -> 'mumbai')
            city_name = city_file.split('/')[0] if '/' in city_file else city_file.replace('.geojson', '')
            file_path = os.path.join(maps_dir, 'Cities', city_name, city_file.split('/')[-1])
        else:
            # Default to Maps directory
            file_path = os.path.join(maps_dir, filename)

        # Check if file exists
        if not os.path.exists(file_path):
            current_app.logger.error(f"GeoJSON file not found: {file_path}")
            abort(404)

        # Serve the file
        directory = os.path.dirname(file_path)
        filename_only = os.path.basename(file_path)
        return send_from_directory(directory, filename_only, mimetype='application/json')

    except Exception as e:
        current_app.logger.error(f"Error serving GeoJSON file {filename}: {str(e)}")
        abort(500)

@bp.route('/about')
def about():
    """About page route."""
    return render_template('about.html')

@bp.route('/contact')
def contact():
    """Contact page route."""
    return render_template('contact.html')

@bp.route('/report-incident')
@login_required
def report_incident():
    """Report an incident page route."""
    return render_template('report_incident.html')

@bp.route('/safety-tips')
def safety_tips():
    """Safety tips and best practices page route."""
    return render_template('safety_tips.html')
