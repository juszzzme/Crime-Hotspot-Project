"""
Visualization API Endpoints

This module provides API endpoints for generating crime data visualizations.
"""
from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required, current_user
import json
import plotly
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from src.visualization.crime_trends import CrimeTrendAnalyzer
from app.models.crime_data import CrimeType

bp = Blueprint('visualization', __name__)

@bp.route('/api/visualization/trend', methods=['GET'])
@login_required
def get_crime_trend():
    """
    Get crime trend visualization data.
    
    Query Parameters:
        time_unit: Time unit for aggregation (D=day, W=week, M=month, Q=quarter, Y=year)
        crime_type_id: Optional filter for specific crime type
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
    """
    try:
        # Parse query parameters
        time_unit = request.args.get('time_unit', 'W').upper()
        crime_type_id = request.args.get('crime_type_id', type=int)
        
        # Parse dates
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
        
        # Initialize analyzer with date range
        analyzer = CrimeTrendAnalyzer(start_date=start_date, end_date=end_date)
        
        # Generate the plot
        fig = analyzer.plot_trend(time_unit=time_unit, crime_type_id=crime_type_id)
        
        # Convert to JSON for frontend
        return jsonify({
            'success': True,
            'plot': json.loads(fig.to_json())
        })
        
    except Exception as e:
        current_app.logger.error(f"Error generating trend visualization: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/api/visualization/seasonal', methods=['GET'])
@login_required
def get_seasonal_analysis():
    """
    Get seasonal decomposition of crime data.
    
    Query Parameters:
        crime_type_id: Optional filter for specific crime type
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
    """
    try:
        # Parse query parameters
        crime_type_id = request.args.get('crime_type_id', type=int)
        
        # Parse dates
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
        
        # Initialize analyzer with date range
        analyzer = CrimeTrendAnalyzer(start_date=start_date, end_date=end_date)
        
        # Generate the plot
        fig = analyzer.plot_seasonal_decomposition(crime_type_id=crime_type_id)
        
        # Convert to JSON for frontend
        return jsonify({
            'success': True,
            'plot': json.loads(fig.to_json())
        })
        
    except Exception as e:
        current_app.logger.error(f"Error generating seasonal analysis: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/api/visualization/heatmap', methods=['GET'])
@login_required
def get_crime_heatmap():
    """
    Get a heatmap of crime data.
    
    Query Parameters:
        x_axis: Column for x-axis (e.g., 'hour_of_day')
        y_axis: Column for y-axis (e.g., 'day_of_week')
        crime_type_id: Optional filter for specific crime type
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
    """
    try:
        from sqlalchemy import extract, func, and_
        from app.models.crime_data import CrimeReport
        import pandas as pd
        
        # Parse query parameters
        x_axis = request.args.get('x_axis', 'hour')
        y_axis = request.args.get('y_axis', 'dow')
        crime_type_id = request.args.get('crime_type_id', type=int)
        
        # Parse dates
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Build the query
        query = db.session.query(
            extract('HOUR', CrimeReport.date_occurred).label('hour'),
            extract('DOW', CrimeReport.date_occurred).label('dow'),
            func.count(CrimeReport.id).label('crime_count')
        )
        
        # Apply filters
        if start_date:
            query = query.filter(CrimeReport.date_occurred >= start_date)
        if end_date:
            query = query.filter(CrimeReport.date_occurred <= end_date)
        if crime_type_id:
            query = query.filter(CrimeReport.crime_type_id == crime_type_id)
        
        # Group by the selected dimensions
        query = query.group_by('hour', 'dow')
        
        # Execute query and convert to DataFrame
        results = query.all()
        df = pd.DataFrame(results, columns=['hour', 'dow', 'crime_count'])
        
        # Map day of week numbers to names
        day_names = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        df['day_of_week'] = df['dow'].apply(lambda x: day_names[int(x)])
        
        # Generate the heatmap
        fig = CrimeTrendAnalyzer.plot_crime_heatmap(
            df,
            x_col='hour',
            y_col='day_of_week',
            title='Crime Distribution by Day and Hour'
        )
        
        # Convert to JSON for frontend
        return jsonify({
            'success': True,
            'plot': json.loads(fig.to_json())
        })
        
    except Exception as e:
        current_app.logger.error(f"Error generating heatmap: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/api/visualization/crime_types', methods=['GET'])
@login_required
def get_crime_types():
    """Get a list of crime types for dropdown menus."""
    try:
        crime_types = CrimeType.query.order_by(CrimeType.category, CrimeType.name).all()
        
        return jsonify({
            'success': True,
            'data': [{
                'id': ct.id,
                'name': f"{ct.category} - {ct.name}",
                'category': ct.category,
                'severity': ct.severity
            } for ct in crime_types]
        })
        
    except Exception as e:
        current_app.logger.error(f"Error fetching crime types: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
