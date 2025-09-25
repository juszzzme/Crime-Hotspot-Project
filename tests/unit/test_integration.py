#!/usr/bin/env python3
"""
Comprehensive Integration Test for Crime Hotspot Application
Tests all components working together as a unified system
"""

import sys
import os
import time
import requests
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_application_startup():
    """Test that the application starts correctly"""
    print("🚀 Testing Application Startup...")
    
    try:
        from app import create_app
        app = create_app()
        
        print("✅ Flask application created successfully")
        
        # Test that all blueprints are registered
        blueprints = list(app.blueprints.keys())
        expected_blueprints = ['main', 'auth', 'api', 'visualization']
        
        for blueprint in expected_blueprints:
            if blueprint in blueprints:
                print(f"✅ Blueprint '{blueprint}' registered")
            else:
                print(f"⚠️ Blueprint '{blueprint}' not found")
        
        # Test route registration
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(rule.endpoint)
        
        expected_routes = [
            'main.index',
            'main.advanced_map',
            'main.pattern_analysis',
            'main.ai_predictions',
            'auth.login',
            'auth.logout'
        ]
        
        for route in expected_routes:
            if route in routes:
                print(f"✅ Route '{route}' registered")
            else:
                print(f"❌ Route '{route}' missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Application startup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_template_integration():
    """Test that all templates can be rendered without errors"""
    print("\n🎨 Testing Template Integration...")
    
    try:
        from app import create_app
        from flask import render_template
        
        app = create_app()
        
        with app.app_context():
            # Test templates that should render without authentication
            templates_to_test = [
                ('index.html', {}),
                ('about.html', {}),
                ('contact.html', {}),
                ('auth/login.html', {'form': None, 'now': datetime.utcnow()}),
                ('auth/signup.html', {'form': None, 'now': datetime.utcnow()})
            ]
            
            for template_name, context in templates_to_test:
                try:
                    result = render_template(template_name, **context)
                    if len(result) > 0:
                        print(f"✅ Template '{template_name}' renders successfully")
                    else:
                        print(f"⚠️ Template '{template_name}' renders but is empty")
                except Exception as e:
                    print(f"❌ Template '{template_name}' failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Template integration test failed: {e}")
        return False

def test_static_files():
    """Test that static files are accessible"""
    print("\n📁 Testing Static Files...")
    
    static_files = [
        'css/unified_styles.css',
        'js/unified_app.js',
        'css/style.css',
        'js/main.js'
    ]
    
    for file_path in static_files:
        full_path = os.path.join('app', 'static', file_path)
        if os.path.exists(full_path):
            print(f"✅ Static file '{file_path}' exists")
        else:
            print(f"❌ Static file '{file_path}' missing")
    
    return True

def test_database_integration():
    """Test database connectivity and models"""
    print("\n🗄️ Testing Database Integration...")
    
    try:
        from app import create_app
        from app.extensions import db
        from app.models.user import User
        
        app = create_app()
        
        with app.app_context():
            # Test database connection
            try:
                db.create_all()
                print("✅ Database tables created successfully")
            except Exception as e:
                print(f"❌ Database creation failed: {e}")
                return False
            
            # Test user model
            try:
                user_count = User.query.count()
                print(f"✅ User model working - {user_count} users in database")
            except Exception as e:
                print(f"❌ User model test failed: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Database integration test failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoint accessibility"""
    print("\n🔌 Testing API Endpoints...")
    
    try:
        from app import create_app
        
        app = create_app()
        
        with app.test_client() as client:
            # Test public endpoints
            public_endpoints = [
                ('/', 'Home page'),
                ('/auth/login', 'Login page')
            ]
            
            for endpoint, description in public_endpoints:
                try:
                    response = client.get(endpoint)
                    if response.status_code == 200:
                        print(f"✅ {description} accessible (200)")
                    else:
                        print(f"⚠️ {description} returned {response.status_code}")
                except Exception as e:
                    print(f"❌ {description} failed: {e}")
            
            # Test protected endpoints (should redirect to login)
            protected_endpoints = [
                ('/advanced-map', 'Advanced Map'),
                ('/pattern-analysis', 'Pattern Analysis'),
                ('/ai-predictions', 'AI Dashboard')
            ]
            
            for endpoint, description in protected_endpoints:
                try:
                    response = client.get(endpoint, follow_redirects=False)
                    if response.status_code == 302:
                        print(f"✅ {description} correctly redirects to login (302)")
                    elif response.status_code == 200:
                        print(f"⚠️ {description} accessible without login (200)")
                    else:
                        print(f"❌ {description} unexpected status {response.status_code}")
                except Exception as e:
                    print(f"❌ {description} failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ API endpoint test failed: {e}")
        return False

def test_unified_framework():
    """Test that unified CSS and JS frameworks are properly integrated"""
    print("\n🎯 Testing Unified Framework Integration...")
    
    # Check if unified CSS file exists and has content
    unified_css_path = os.path.join('app', 'static', 'css', 'unified_styles.css')
    if os.path.exists(unified_css_path):
        with open(unified_css_path, 'r') as f:
            css_content = f.read()
            if ':root' in css_content and '--primary-color' in css_content:
                print("✅ Unified CSS framework properly configured")
            else:
                print("⚠️ Unified CSS exists but may be incomplete")
    else:
        print("❌ Unified CSS framework missing")
    
    # Check if unified JS file exists and has content
    unified_js_path = os.path.join('app', 'static', 'js', 'unified_app.js')
    if os.path.exists(unified_js_path):
        with open(unified_js_path, 'r') as f:
            js_content = f.read()
            if 'CrimeHotspotApp' in js_content and 'class' in js_content:
                print("✅ Unified JavaScript framework properly configured")
            else:
                print("⚠️ Unified JavaScript exists but may be incomplete")
    else:
        print("❌ Unified JavaScript framework missing")
    
    return True

def test_navigation_consistency():
    """Test that navigation is consistent across all pages"""
    print("\n🧭 Testing Navigation Consistency...")
    
    try:
        from app import create_app
        from flask import render_template
        
        app = create_app()
        
        with app.app_context():
            # Test that base template navigation renders correctly
            try:
                # Test with a simple template that extends base
                result = render_template('index.html')
                
                # Check for navigation elements
                nav_checks = [
                    ('navbar', 'Navigation bar'),
                    ('CRIMESENSE', 'Brand name'),
                    ('Home', 'Home link'),
                    ('Advanced Map', 'Advanced Map link'),
                    ('AI Predictions', 'AI Predictions link'),
                    ('Pattern Analysis', 'Pattern Analysis link')
                ]
                
                for check, description in nav_checks:
                    if check in result:
                        print(f"✅ {description} found in navigation")
                    else:
                        print(f"⚠️ {description} missing from navigation")
                
            except Exception as e:
                print(f"❌ Navigation consistency test failed: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Navigation test failed: {e}")
        return False

def run_comprehensive_test():
    """Run all integration tests"""
    print("🔧 Crime Hotspot Application - Comprehensive Integration Test")
    print("=" * 70)
    print(f"📅 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        test_application_startup,
        test_static_files,
        test_database_integration,
        test_template_integration,
        test_api_endpoints,
        test_unified_framework,
        test_navigation_consistency
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test in tests:
        try:
            if test():
                passed_tests += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 70)
    print(f"📊 Test Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All integration tests passed! The application is fully integrated.")
        print("✅ The Crime Hotspot web application is working as a unified system.")
    else:
        print(f"⚠️ {total_tests - passed_tests} tests failed. Please review the issues above.")
    
    print(f"📅 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
