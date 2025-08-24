#!/usr/bin/env python3
"""
Test template rendering to identify issues
"""

try:
    print("Testing template rendering...")
    from app import create_app
    from flask import render_template
    
    app = create_app()
    
    with app.app_context():
        print("Testing index template...")
        try:
            result = render_template('index.html')
            print(f"✅ Index template rendered successfully ({len(result)} chars)")
        except Exception as e:
            print(f"❌ Index template failed: {e}")
            import traceback
            traceback.print_exc()
        
        print("\nTesting map template...")
        try:
            result = render_template('map.html', view_type='country', location_id='india')
            print(f"✅ Map template rendered successfully ({len(result)} chars)")
        except Exception as e:
            print(f"❌ Map template failed: {e}")
            import traceback
            traceback.print_exc()
        
        print("\nTesting AI predictions template...")
        try:
            result = render_template('ai_predictions.html')
            print(f"✅ AI predictions template rendered successfully ({len(result)} chars)")
        except Exception as e:
            print(f"❌ AI predictions template failed: {e}")
            import traceback
            traceback.print_exc()
    
    print("✅ Template tests completed")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
