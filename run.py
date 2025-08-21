#!/usr/bin/env python3
"""
Crime Hotspot Map - Main Application Entry Point
"""
import os
from app import create_app

# Create the application instance
app = create_app()

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the application
    app.run(host='0.0.0.0', port=port, debug=True)
