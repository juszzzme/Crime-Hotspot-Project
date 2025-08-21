from datetime import datetime
from flask import Blueprint, render_template, request, current_app, abort, redirect, url_for, send_from_directory
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
def map_view():
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
    # Normalize names for file lookup
    state_name_normalized = state_name.lower().replace(' ', '-')
    city_name_normalized = city_name.lower().replace(' ', '-')
    
    # Check if city exists
    city_file_path = os.path.join(current_app.root_path, '..', 'Maps', 'Cities', city_name_normalized, f"{city_name_normalized}.geojson")
    if not os.path.exists(city_file_path):
        current_app.logger.error(f"City file not found: {city_file_path}")
        abort(404)
    
    return render_template('map.html', view_type='city', location_id=city_name_normalized,
                           state_name=state_name, location_name=city_name)

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

@bp.route('/about')
def about():
    """About page route."""
    return render_template('about.html')

@bp.route('/contact')
def contact():
    """Contact page route."""
    return render_template('contact.html')
