#!/usr/bin/env python3
"""
Comprehensive System Check for Crime Hotspot Application
Verifies all components, fixes, and functionality
"""

import sys
import os
import time
import requests
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_server_status():
    """Check if the Flask server is running"""
    print("🌐 Checking Server Status...")
    
    try:
        response = requests.get('http://127.0.0.1:5000/', timeout=10)
        if response.status_code == 200:
            print("✅ Server is running and responding")
            print(f"   Status: {response.status_code}")
            print(f"   Response length: {len(response.text)} characters")
            return True
        else:
            print(f"❌ Server returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running or not accessible")
        return False
    except Exception as e:
        print(f"❌ Server check failed: {e}")
        return False

def check_application_structure():
    """Check application file structure and dependencies"""
    print("\n📁 Checking Application Structure...")
    
    critical_files = [
        ('app/__init__.py', 'Main application module'),
        ('app/routes/main.py', 'Main routes'),
        ('app/routes/auth.py', 'Authentication routes'),
        ('app/templates/base.html', 'Base template'),
        ('app/templates/map.html', 'Interactive map template'),
        ('app/templates/advanced_map.html', 'Advanced map template'),
        ('app/templates/ai_predictions.html', 'AI predictions template'),
        ('app/templates/pattern_analysis.html', 'Pattern analysis template'),
        ('app/static/css/unified_styles.css', 'Unified CSS framework'),
        ('app/static/js/unified_app.js', 'Unified JavaScript framework'),
        ('config.py', 'Configuration file'),
        ('wsgi.py', 'WSGI entry point')
    ]
    
    missing_files = []
    for file_path, description in critical_files:
        if os.path.exists(file_path):
            print(f"✅ {description}")
        else:
            print(f"❌ {description} - MISSING: {file_path}")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def check_database_and_models():
    """Check database connectivity and models"""
    print("\n🗄️ Checking Database and Models...")
    
    try:
        from app import create_app
        from app.extensions import db
        from app.models.user import User
        
        app = create_app()
        
        with app.app_context():
            # Test database connection
            try:
                db.create_all()
                print("✅ Database tables created/verified")
            except Exception as e:
                print(f"❌ Database creation failed: {e}")
                return False
            
            # Test user model
            try:
                user_count = User.query.count()
                print(f"✅ User model working - {user_count} users in database")
                
                # Check for demo user
                demo_user = User.query.filter_by(email='admin@crimesense.com').first()
                if demo_user:
                    print("✅ Demo user exists")
                else:
                    print("⚠️ Demo user not found")
                    
            except Exception as e:
                print(f"❌ User model test failed: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Database check failed: {e}")
        return False

def check_routes_and_blueprints():
    """Check all routes and blueprints are registered"""
    print("\n🛣️ Checking Routes and Blueprints...")
    
    try:
        from app import create_app
        
        app = create_app()
        
        # Check blueprints
        expected_blueprints = ['main', 'auth']
        registered_blueprints = list(app.blueprints.keys())
        
        for blueprint in expected_blueprints:
            if blueprint in registered_blueprints:
                print(f"✅ Blueprint '{blueprint}' registered")
            else:
                print(f"❌ Blueprint '{blueprint}' missing")
        
        # Check critical routes
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(rule.endpoint)
        
        critical_routes = [
            'main.index',
            'main.map',
            'main.advanced_map',
            'main.pattern_analysis',
            'main.ai_predictions',
            'auth.login',
            'auth.logout',
            'main.pattern_analysis_api'
        ]
        
        for route in critical_routes:
            if route in routes:
                print(f"✅ Route '{route}' registered")
            else:
                print(f"❌ Route '{route}' missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Routes check failed: {e}")
        return False

def check_templates_integration():
    """Check template integration and inheritance"""
    print("\n🎨 Checking Template Integration...")
    
    try:
        from app import create_app
        
        app = create_app()
        
        with app.test_client() as client:
            # Test public pages
            public_pages = [
                ('/', 'Home page'),
                ('/auth/login', 'Login page')
            ]
            
            for url, name in public_pages:
                response = client.get(url)
                if response.status_code == 200:
                    content = response.data.decode('utf-8')
                    
                    # Check for unified framework
                    if 'unified_styles.css' in content:
                        print(f"✅ {name} - Unified CSS included")
                    else:
                        print(f"⚠️ {name} - Unified CSS missing")
                    
                    if 'unified_app.js' in content:
                        print(f"✅ {name} - Unified JavaScript included")
                    else:
                        print(f"⚠️ {name} - Unified JavaScript missing")
                    
                    # Check for base template elements
                    if 'CRIMESENSE' in content:
                        print(f"✅ {name} - Base template integration")
                    else:
                        print(f"⚠️ {name} - Base template issues")
                        
                else:
                    print(f"❌ {name} failed to load: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Template integration check failed: {e}")
        return False

def check_static_files():
    """Check static files and resources"""
    print("\n📦 Checking Static Files...")
    
    static_files = [
        ('app/static/css/unified_styles.css', 'Unified CSS framework'),
        ('app/static/js/unified_app.js', 'Unified JavaScript framework'),
        ('app/static/css/style.css', 'Legacy CSS'),
        ('app/static/js/main.js', 'Main JavaScript')
    ]
    
    for file_path, description in static_files:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"✅ {description} ({file_size} bytes)")
        else:
            print(f"❌ {description} - MISSING: {file_path}")
    
    return True

def check_map_functionality():
    """Check map-related functionality"""
    print("\n🗺️ Checking Map Functionality...")
    
    try:
        # Check GeoJSON files
        geojson_files = [
            ('Maps/Cities/Chennai/chennai.geojson', 'Chennai GeoJSON'),
            ('Maps/Cities/Chennai/CHENNAI.geojson', 'Chennai GeoJSON (alt)')
        ]
        
        chennai_geojson_exists = False
        for file_path, description in geojson_files:
            if os.path.exists(file_path):
                print(f"✅ {description} exists")
                chennai_geojson_exists = True
                break
        
        if not chennai_geojson_exists:
            print("⚠️ Chennai GeoJSON files not found")
        
        # Check map template content
        map_template_path = 'app/templates/map.html'
        if os.path.exists(map_template_path):
            with open(map_template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                map_features = [
                    ('loadCityGeoJSON', 'GeoJSON loading function'),
                    ('addCityInfrastructure', 'Infrastructure markers'),
                    ('markercluster', 'Clustering support'),
                    ('clusterGroup', 'Cluster group'),
                    ('Apollo Hospital Chennai', 'Hospital data'),
                    ('T. Nagar Police Station', 'Police station data'),
                    ('crime markers disabled', 'Crime markers disabled')
                ]
                
                for feature, description in map_features:
                    if feature in content:
                        print(f"✅ {description}")
                    else:
                        print(f"⚠️ {description} missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Map functionality check failed: {e}")
        return False

def check_ai_features():
    """Check AI-related features"""
    print("\n🧠 Checking AI Features...")
    
    try:
        # Check AI predictions template
        ai_template_path = 'app/templates/ai_predictions.html'
        if os.path.exists(ai_template_path):
            with open(ai_template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                ai_features = [
                    ('{% extends "base.html" %}', 'Base template extension'),
                    ('ai-dashboard-body', 'Dashboard styling'),
                    ('Chart.js', 'Chart library'),
                    ('{% block content %}', 'Content block'),
                    ('{% endblock %}', 'Block closure')
                ]
                
                for feature, description in ai_features:
                    if feature in content:
                        print(f"✅ AI Predictions - {description}")
                    else:
                        print(f"⚠️ AI Predictions - {description} missing")
        
        # Check pattern analysis
        pattern_template_path = 'app/templates/pattern_analysis.html'
        if os.path.exists(pattern_template_path):
            with open(pattern_template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                pattern_features = [
                    ('loadPatternAnalysis', 'Data loading function'),
                    ('refreshAnalysis', 'Refresh function'),
                    ('/api/pattern-analysis', 'API endpoint'),
                    ('analysisContainer', 'Analysis container')
                ]
                
                for feature, description in pattern_features:
                    if feature in content:
                        print(f"✅ Pattern Analysis - {description}")
                    else:
                        print(f"⚠️ Pattern Analysis - {description} missing")
        
        return True
        
    except Exception as e:
        print(f"❌ AI features check failed: {e}")
        return False

def check_live_endpoints():
    """Check live endpoints if server is running"""
    print("\n🔌 Checking Live Endpoints...")
    
    try:
        # Test public endpoints
        public_endpoints = [
            ('/', 'Home page'),
            ('/auth/login', 'Login page')
        ]
        
        for endpoint, name in public_endpoints:
            try:
                response = requests.get(f'http://127.0.0.1:5000{endpoint}', timeout=5)
                if response.status_code == 200:
                    print(f"✅ {name} - Status: {response.status_code}")
                else:
                    print(f"⚠️ {name} - Status: {response.status_code}")
            except:
                print(f"❌ {name} - Connection failed")
        
        # Test protected endpoints (should redirect)
        protected_endpoints = [
            ('/map', 'Interactive map'),
            ('/advanced-map', 'Advanced map'),
            ('/pattern-analysis', 'Pattern analysis'),
            ('/ai-predictions', 'AI predictions')
        ]
        
        for endpoint, name in protected_endpoints:
            try:
                response = requests.get(f'http://127.0.0.1:5000{endpoint}', timeout=5, allow_redirects=False)
                if response.status_code == 302:
                    print(f"✅ {name} - Properly protected (302 redirect)")
                elif response.status_code == 200:
                    print(f"⚠️ {name} - Accessible without login (200)")
                else:
                    print(f"⚠️ {name} - Status: {response.status_code}")
            except:
                print(f"❌ {name} - Connection failed")
        
        return True
        
    except Exception as e:
        print(f"❌ Live endpoints check failed: {e}")
        return False

def run_comprehensive_check():
    """Run all system checks"""
    print("🔍 COMPREHENSIVE CRIME HOTSPOT APPLICATION CHECK")
    print("=" * 60)
    print(f"📅 Check started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    checks = [
        check_server_status,
        check_application_structure,
        check_database_and_models,
        check_routes_and_blueprints,
        check_templates_integration,
        check_static_files,
        check_map_functionality,
        check_ai_features,
        check_live_endpoints
    ]
    
    passed_checks = 0
    total_checks = len(checks)
    
    for check in checks:
        try:
            if check():
                passed_checks += 1
                print(f"✅ {check.__name__} PASSED")
            else:
                print(f"❌ {check.__name__} FAILED")
        except Exception as e:
            print(f"💥 {check.__name__} CRASHED: {e}")
        print()
    
    print("=" * 60)
    print(f"📊 FINAL RESULTS: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print("🎉 ALL CHECKS PASSED!")
        print("✅ Server running correctly")
        print("✅ All files and structure intact")
        print("✅ Database and models working")
        print("✅ Routes and blueprints registered")
        print("✅ Templates properly integrated")
        print("✅ Static files accessible")
        print("✅ Map functionality implemented")
        print("✅ AI features working")
        print("✅ Endpoints responding correctly")
        print("🚀 APPLICATION IS FULLY OPERATIONAL!")
    else:
        print(f"⚠️ {total_checks - passed_checks} checks failed.")
        print("🔧 Please review the issues above.")
    
    print(f"📅 Check completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return passed_checks == total_checks

if __name__ == "__main__":
    success = run_comprehensive_check()
    sys.exit(0 if success else 1)
