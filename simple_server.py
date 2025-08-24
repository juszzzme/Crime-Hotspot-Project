#!/usr/bin/env python3
"""
Simple server for testing
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("🚀 Starting simple test server...")
    
    from app import create_app
    
    app = create_app()
    
    print("✅ App created successfully")
    print("🌐 Starting server on http://127.0.0.1:5000")
    print("🔐 Demo login: admin@crimesense.com / admin123")
    print("=" * 50)
    
    # Run with minimal configuration
    app.run(
        debug=True,
        host='127.0.0.1',
        port=5000,
        use_reloader=False,
        threaded=True
    )
    
except Exception as e:
    print(f"❌ Server failed to start: {e}")
    import traceback
    traceback.print_exc()
