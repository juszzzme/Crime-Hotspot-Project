from flask import Blueprint, jsonify, request, current_app, send_file
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime, timedelta
import json
import os
import csv
import io
import numpy as np
from werkzeug.security import generate_password_hash
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.models.crime_prediction import CrimePredictionEngine

bp = Blueprint('api', __name__)

# Initialize prediction engine
prediction_engine = None

def get_prediction_engine():
    """Get or initialize the prediction engine."""
    global prediction_engine
    if prediction_engine is None:
        try:
            prediction_engine = CrimePredictionEngine()
            # Train models on startup
            prediction_engine.train_prediction_models()
        except Exception as e:
            current_app.logger.error(f"Failed to initialize prediction engine: {e}")
            prediction_engine = None
    return prediction_engine

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            return jsonify({"error": "Admin access required"}), 403
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/crime-data', methods=['GET'])
@login_required
def get_crime_data():
    """Get crime data with optional filtering."""
    try:
        # Get query parameters
        state = request.args.get('state')
        city = request.args.get('city')
        crime_type = request.args.get('crime_type')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        limit = int(request.args.get('limit', 100))

        # Generate sample crime data (replace with actual database query)
        from app.routes.main import generate_sample_crime_data
        sample_data = generate_sample_crime_data()

        # Apply filters if provided
        filtered_data = sample_data
        if state:
            filtered_data = [d for d in filtered_data if state.lower() in d.get('location', '').lower()]
        if crime_type:
            filtered_data = [d for d in filtered_data if d.get('crime_type') == crime_type]

        # Limit results
        filtered_data = filtered_data[:limit]

        return jsonify({
            'success': True,
            'data': filtered_data,
            'total': len(filtered_data),
            'filters': {
                'state': state,
                'city': city,
                'crime_type': crime_type,
                'start_date': start_date,
                'end_date': end_date
            }
        })

    except Exception as e:
        current_app.logger.error(f"Error fetching crime data: {str(e)}")
        return jsonify({"error": "Failed to fetch crime data"}), 500

@bp.route('/states', methods=['GET'])
def get_states():
    """Get list of all states with basic crime stats."""
    try:
        # TODO: Replace with actual database query
        states = [
            {"id": 1, "name": "Tamil Nadu", "crime_count": 1245},
            {"id": 2, "name": "Maharashtra", "crime_count": 1987},
            # Add more states as needed
        ]
        return jsonify(states)
    except Exception as e:
        current_app.logger.error(f"Error fetching states: {str(e)}")
        return jsonify({"error": "Failed to fetch states data"}), 500

@bp.route('/state/<int:state_id>/hotspots', methods=['GET'])
@login_required
def get_state_hotspots(state_id):
    """Get crime hotspots for a specific state."""
    try:
        # TODO: Add actual data processing
        return jsonify({"state_id": state_id, "hotspots": []})
    except Exception as e:
        current_app.logger.error(f"Error fetching state hotspots: {str(e)}")
        return jsonify({"error": "Failed to fetch state hotspots"}), 500

@bp.route('/city/<int:city_id>/hotspots', methods=['GET'])
@login_required
def get_city_hotspots(city_id):
    """Get detailed crime data for a specific city."""
    try:
        # TODO: Add actual data processing
        return jsonify({"city_id": city_id, "hotspots": [], "stats": {}})
    except Exception as e:
        current_app.logger.error(f"Error fetching city hotspots: {str(e)}")
        return jsonify({"error": "Failed to fetch city hotspots"}), 500

@bp.route('/crime-stats', methods=['GET'])
@login_required
def get_crime_statistics():
    """Get aggregated crime statistics with filtering options."""
    try:
        # Get query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        crime_type = request.args.get('crime_type')
        location = request.args.get('location')
        
        # TODO: Replace with actual database queries
        # This is a mock response
        stats = {
            "total_crimes": 1245,
            "crimes_by_type": {
                "Theft": 350,
                "Assault": 280,
                "Burglary": 195,
                "Robbery": 150,
                "Other": 270
            },
            "trends": {
                "last_30_days": [45, 52, 48, 60, 55, 58, 62],
                "labels": [str(datetime.now().date() - timedelta(days=i)) for i in range(6, -1, -1)]
            },
            "hotspots": [
                {"location": "Downtown", "count": 320, "lat": 13.0827, "lng": 80.2707},
                {"location": "Suburb A", "count": 280, "lat": 13.0827, "lng": 80.2807},
                {"location": "Suburb B", "count": 210, "lat": 13.0727, "lng": 80.2607}
            ]
        }
        
        return jsonify(stats)
        
    except Exception as e:
        current_app.logger.error(f"Error fetching crime statistics: {str(e)}")
        return jsonify({"error": "Failed to fetch crime statistics"}), 500

@bp.route('/export/csv', methods=['GET'])
@login_required
def export_to_csv():
    """Export crime data as CSV."""
    try:
        # Get query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # TODO: Replace with actual database query
        # Mock data
        data = [
            {"id": 1, "type": "Theft", "date": "2023-01-15", "location": "Downtown", "status": "Open"},
            {"id": 2, "type": "Assault", "date": "2023-01-16", "location": "Suburb A", "status": "Closed"},
            {"id": 3, "type": "Burglary", "date": "2023-01-17", "location": "Suburb B", "status": "Open"}
        ]
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["id", "type", "date", "location", "status"])
        writer.writeheader()
        writer.writerows(data)
        
        # Create response with CSV file
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'crime_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
        
    except Exception as e:
        current_app.logger.error(f"Error exporting data to CSV: {str(e)}")
        return jsonify({"error": "Failed to export data"}), 500

@bp.route('/api/search', methods=['GET'])
@login_required
def search_crimes():
    """Search crimes with filters."""
    try:
        query = request.args.get('q', '')
        crime_type = request.args.get('type')
        status = request.args.get('status')
        
        # TODO: Replace with actual database query
        # Mock response
        results = [
            {"id": 1, "title": f"{crime_type} reported" if crime_type else "Crime reported", "type": crime_type or "Theft", "date": "2023-01-15"}
            for _ in range(5)  # Return 5 mock results
        ]
        
        return jsonify({"results": results, "count": len(results)})
        
    except Exception as e:
        current_app.logger.error(f"Error searching crimes: {str(e)}")
        return jsonify({"error": "Search failed"}), 500

@bp.route('/safe-route', methods=['POST'])
@login_required
def get_safe_route():
    """Calculate safe route between two points."""
    try:
        data = request.get_json()
        start = data.get('start')  # {lat: x, lng: y}
        end = data.get('end')
        
        if not start or not end:
            return jsonify({"error": "Start and end points are required"}), 400
            
        # TODO: Implement route calculation
        return jsonify({
            "route": [],
            "warnings": [],
            "safety_score": 0.0
        })
    except Exception as e:
        current_app.logger.error(f"Error calculating safe route: {str(e)}")
        return jsonify({"error": "Failed to calculate safe route"}), 500

# ====================================
# AI PREDICTION ENDPOINTS
# ====================================
# Clean slate - new implementation will go here



def get_safety_recommendations(risk_level: str) -> list:
    """Get safety recommendations based on risk level."""
    recommendations = {
        'Low': [
            'Maintain current security measures',
            'Continue community policing programs',
            'Regular safety awareness campaigns'
        ],
        'Medium': [
            'Increase police patrols during peak hours',
            'Improve street lighting in vulnerable areas',
            'Establish neighborhood watch programs',
            'Install CCTV cameras at key locations'
        ],
        'High': [
            'Deploy additional police personnel',
            'Implement emergency response protocols',
            'Conduct intensive community outreach',
            'Coordinate with local authorities for immediate action',
            'Consider temporary security measures'
        ]
    }

    return recommendations.get(risk_level, ['Monitor situation closely'])
