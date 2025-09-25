#!/usr/bin/env python3
"""
Test app creation to identify issues
"""

try:
    print("Testing app creation...")
    from app import create_app
    
    print("Creating app...")
    app = create_app()
    
    print("✅ App created successfully")
    
    # Test routes
    with app.app_context():
        print("Testing routes...")
        for rule in app.url_map.iter_rules():
            if 'map' in rule.endpoint:
                print(f"Map route: {rule.endpoint} -> {rule.rule}")
    
    print("✅ All tests passed")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
