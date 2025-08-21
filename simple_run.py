#!/usr/bin/env python3
"""
Simple version of CRIMESENSE app without database dependencies
"""
import os
from flask import Flask, render_template, send_from_directory, abort, redirect

# Create Flask app
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

# Routes
@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page."""
    return render_template('about.html')

@app.route('/contact')
def contact():
    """Contact page."""
    return render_template('contact.html')

@app.route('/map')
def map_view():
    """Map page - country view."""
    return render_template('map.html', view_type='country', location_id='india')

@app.route('/map/state/<state_name>')
def state_map_view(state_name):
    """Map page - state view."""
    return render_template('map.html', view_type='state', location_id=state_name, location_name=state_name)

@app.route('/map/city/<state_name>/<city_name>')
def city_map_view(state_name, city_name):
    """Map page - city view."""
    return render_template('map.html', view_type='city', location_id=city_name,
                           state_name=state_name, location_name=city_name)

@app.route('/login')
def login():
    """Login page."""
    return render_template('auth/login.html')

@app.route('/signup')
def signup():
    """Signup page."""
    return render_template('auth/signup.html')

@app.route('/logout')
def logout():
    """Logout route."""
    return redirect('/')

@app.route('/static/geojson/<path:filename>')
def serve_geojson(filename):
    """Serve GeoJSON files from the Maps directory."""
    try:
        # Get the project root directory
        project_root = os.path.dirname(os.path.abspath(__file__))
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
            # Extract city name from path
            city_name = city_file.split('/')[0] if '/' in city_file else city_file.replace('.geojson', '')
            file_path = os.path.join(maps_dir, 'Cities', city_name, city_file.split('/')[-1])
        else:
            # Default to Maps directory
            file_path = os.path.join(maps_dir, filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"GeoJSON file not found: {file_path}")
            abort(404)
        
        # Serve the file
        directory = os.path.dirname(file_path)
        filename_only = os.path.basename(file_path)
        return send_from_directory(directory, filename_only, mimetype='application/json')
        
    except Exception as e:
        print(f"Error serving GeoJSON file {filename}: {str(e)}")
        abort(500)

# Template context processors to provide url_for functionality
@app.context_processor
def utility_processor():
    def mock_url_for(endpoint, **values):
        """Mock url_for function for templates."""
        if endpoint == 'main.index':
            return '/'
        elif endpoint == 'main.about':
            return '/about'
        elif endpoint == 'main.contact':
            return '/contact'
        elif endpoint == 'main.map_view':
            return '/map'
        elif endpoint == 'main.state_map_view':
            state_name = values.get('state_name', 'state')
            return f'/map/state/{state_name}'
        elif endpoint == 'main.city_map_view':
            state_name = values.get('state_name', 'state')
            city_name = values.get('city_name', 'city')
            return f'/map/city/{state_name}/{city_name}'
        elif endpoint == 'auth.login':
            return '/login'
        elif endpoint == 'auth.signup':
            return '/signup'
        elif endpoint == 'auth.logout':
            return '/logout'
        else:
            return '#'

    def mock_csrf_token():
        """Mock CSRF token function."""
        return 'mock-csrf-token'

    return dict(url_for=mock_url_for, csrf_token=mock_csrf_token)

# Mock current_user for templates
@app.context_processor
def inject_user():
    class MockUser:
        is_authenticated = False
        def get_full_name(self):
            return "Guest User"
    
    return dict(current_user=MockUser())

if __name__ == '__main__':
    print("🚀 Starting CRIMESENSE Application...")
    print("📍 Available routes:")
    print("   http://127.0.0.1:5000/ - Home page")
    print("   http://127.0.0.1:5000/about - About page")
    print("   http://127.0.0.1:5000/contact - Contact page")
    print("   http://127.0.0.1:5000/map - Interactive crime map")
    print("   http://127.0.0.1:5000/login - Login page")
    print("   http://127.0.0.1:5000/signup - Sign up page")
    print("\n🗺️  GeoJSON files served from /static/geojson/")
    print("💡 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
