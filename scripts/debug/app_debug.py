#!/usr/bin/env python3
"""
Debug script to identify and fix application issues
"""

import sys
import traceback

def test_imports():
    """Test all critical imports"""
    print("🔍 Testing imports...")
    
    try:
        from app import create_app
        print("✅ Main app import successful")
    except Exception as e:
        print(f"❌ Main app import failed: {e}")
        traceback.print_exc()
        return False
    
    try:
        app = create_app()
        print("✅ App creation successful")
    except Exception as e:
        print(f"❌ App creation failed: {e}")
        traceback.print_exc()
        return False
    
    return True

def test_routes():
    """Test route registration"""
    print("\n🔍 Testing routes...")
    
    try:
        from app import create_app
        app = create_app()
        
        with app.app_context():
            # List all registered routes
            print("📋 Registered routes:")
            for rule in app.url_map.iter_rules():
                print(f"  {rule.endpoint}: {rule.rule} [{', '.join(rule.methods)}]")
        
        print("✅ Route registration successful")
        return True
        
    except Exception as e:
        print(f"❌ Route testing failed: {e}")
        traceback.print_exc()
        return False

def test_database():
    """Test database initialization"""
    print("\n🔍 Testing database...")
    
    try:
        from app import create_app
        from app.extensions import db
        
        app = create_app()
        
        with app.app_context():
            # Try to create tables
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Test user model
            from app.models.user import User
            user_count = User.query.count()
            print(f"✅ User count: {user_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database testing failed: {e}")
        traceback.print_exc()
        return False

def test_templates():
    """Test template rendering"""
    print("\n🔍 Testing templates...")
    
    try:
        from app import create_app
        from flask import render_template_string
        
        app = create_app()
        
        with app.app_context():
            # Test basic template rendering
            result = render_template_string("Hello {{ name }}!", name="World")
            print(f"✅ Template rendering successful: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Template testing failed: {e}")
        traceback.print_exc()
        return False

def run_simple_server():
    """Run a simple Flask server for testing"""
    print("\n🚀 Starting simple test server...")
    
    try:
        from app import create_app
        
        app = create_app()
        
        @app.route('/test')
        def test_route():
            return "✅ Test route working!"
        
        print("🌐 Starting server on http://127.0.0.1:5000")
        print("🔗 Test URL: http://127.0.0.1:5000/test")
        print("🔐 Login URL: http://127.0.0.1:5000/auth/login")
        print("📊 AI Dashboard: http://127.0.0.1:5000/ai-predictions")
        print("🗺️ Advanced Map: http://127.0.0.1:5000/advanced-map")
        print("🧠 Pattern Analysis: http://127.0.0.1:5000/pattern-analysis")
        
        app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
        
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Main debug function"""
    print("🔧 Crime Hotspot Application Debug Tool")
    print("=" * 50)
    
    # Run all tests
    tests = [
        test_imports,
        test_routes,
        test_database,
        test_templates
    ]
    
    all_passed = True
    for test in tests:
        if not test():
            all_passed = False
            print(f"\n❌ Test {test.__name__} failed!")
        else:
            print(f"\n✅ Test {test.__name__} passed!")
    
    if all_passed:
        print("\n🎉 All tests passed! Starting server...")
        run_simple_server()
    else:
        print("\n💥 Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
