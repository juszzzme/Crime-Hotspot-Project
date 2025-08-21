#!/usr/bin/env python3
"""
Test script to verify the CRIMESENSE application functionality
"""
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from flask import Flask, render_template
    print("✓ Flask imported successfully")

    # Test if we can import our config
    try:
        from config import Config
        print("✓ Config imported successfully")
    except Exception as e:
        print(f"✗ Config import failed: {e}")

    # Test basic Flask app with templates
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    app.config.from_object(Config)

    @app.route('/')
    def home():
        try:
            return render_template('index.html')
        except Exception as e:
            return f"Template error: {e}"

    @app.route('/about')
    def about():
        try:
            return render_template('about.html')
        except Exception as e:
            return f"About template error: {e}"

    @app.route('/contact')
    def contact():
        try:
            return render_template('contact.html')
        except Exception as e:
            return f"Contact template error: {e}"

    @app.route('/map')
    def map_view():
        try:
            return render_template('map.html', view_type='country', location_id='india')
        except Exception as e:
            return f"Map template error: {e}"

    @app.route('/test-geojson')
    def test_geojson():
        # Check if Maps directory exists
        maps_dir = os.path.join(os.path.dirname(__file__), 'Maps')
        if os.path.exists(maps_dir):
            files = os.listdir(maps_dir)[:10]  # Show first 10 files
            return f"✓ Maps directory exists with {len(os.listdir(maps_dir))} files. Sample: {files}"
        else:
            return "✗ Maps directory not found"

    @app.route('/static/geojson/<path:filename>')
    def serve_geojson(filename):
        """Test route for serving GeoJSON files."""
        try:
            project_root = os.path.dirname(__file__)
            maps_dir = os.path.join(project_root, 'Maps')

            if filename == 'india.geojson':
                file_path = os.path.join(maps_dir, 'india.geojson')
            else:
                file_path = os.path.join(maps_dir, filename)

            if os.path.exists(file_path):
                return f"✓ GeoJSON file found: {filename}"
            else:
                return f"✗ GeoJSON file not found: {filename}"
        except Exception as e:
            return f"✗ Error serving GeoJSON: {e}"

    if __name__ == '__main__':
        print("Starting CRIMESENSE test app...")
        print("Available routes:")
        print("  / - Home page")
        print("  /about - About page")
        print("  /contact - Contact page")
        print("  /map - Map page")
        print("  /test-geojson - Test GeoJSON files")
        print("  /static/geojson/india.geojson - Test GeoJSON serving")
        app.run(host='0.0.0.0', port=5000, debug=True)

except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Please install required packages:")
    print("pip install Flask")
