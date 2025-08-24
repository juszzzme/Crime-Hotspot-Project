#!/usr/bin/env python3
"""
Simple server runner with verbose output
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("🚀 Starting Crime Hotspot Flask Server...")
    print("📍 Importing application...")
    
    from app import create_app
    
    print("✅ Application imported successfully")
    print("🔧 Creating Flask app...")
    
    app = create_app()
    
    print("✅ Flask app created successfully")
    print("🌐 Starting development server...")
    print("📍 URL: http://127.0.0.1:5000")
    print("🔐 Login: admin@crimesense.com / admin123")
    print("=" * 50)
    
    # Run the app with verbose output
    app.run(
        debug=True,
        host='127.0.0.1',
        port=5000,
        use_reloader=False  # Disable reloader to avoid issues
    )
    
except Exception as e:
    print(f"❌ Error starting server: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
