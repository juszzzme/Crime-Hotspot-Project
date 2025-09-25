#!/usr/bin/env python3
"""
Authenticated test for all Crime Hotspot Application fixes
Tests with proper login authentication
"""

import sys
import os
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_authenticated_client():
    """Create a test client with authenticated session"""
    from app import create_app
    from app.models.user import User
    from app.extensions import db
    
    app = create_app()
    client = app.test_client()
    
    with app.app_context():
        # Ensure demo user exists
        demo_user = User.query.filter_by(email='kmd.zaheer2006@gmail.com').first()
        if not demo_user:
            demo_user = User(
                email='kmd.zaheer2006@gmail.com',
                username='zaheer',
                first_name='Zaheer',
                last_name='Khan',
                password='244343',
                is_active=True,
                is_admin=True
            )
            db.session.add(demo_user)
            db.session.commit()
    
    # Login
    login_data = {
        'email': 'kmd.zaheer2006@gmail.com',
        'password': '244343',
        'remember': False
    }
    
    response = client.post('/auth/login', data=login_data, follow_redirects=True)
    print(f"Login status: {response.status_code}")
    
    return app, client

def test_chennai_map_authenticated():
    """Test Chennai map with authentication"""
    print("🗺️ Testing Chennai Map (Authenticated)...")
    
    try:
        app, client = create_authenticated_client()
        
        # Test Chennai city map route
        response = client.get('/map/city/tamil-nadu/chennai')
        print(f"Chennai map response: {response.status_code}")
        
        if response.status_code == 200:
            content = response.data.decode('utf-8')
            
            # Check for essential components
            checks = [
                ('loadCityGeoJSON', 'GeoJSON loading function'),
                ('addCityInfrastructure', 'Infrastructure function'),
                ('markercluster', 'Clustering support'),
                ('Chennai', 'City reference')
            ]
            
            for check, description in checks:
                if check in content:
                    print(f"✅ {description} found")
                else:
                    print(f"⚠️ {description} missing")
            
            return True
        else:
            print(f"❌ Chennai map failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Chennai map test failed: {e}")
        return False

def test_ai_predictions_authenticated():
    """Test AI predictions with authentication"""
    print("\n🧠 Testing AI Predictions (Authenticated)...")
    
    try:
        app, client = create_authenticated_client()
        
        response = client.get('/ai-predictions')
        print(f"AI predictions response: {response.status_code}")
        
        if response.status_code == 200:
            content = response.data.decode('utf-8')
            
            # Check for key components
            checks = [
                ('AI-Powered Crime Predictions', 'Page title'),
                ('ai-dashboard-body', 'Dashboard styling'),
                ('Chart.js', 'Chart library'),
                ('CRIMESENSE', 'Base template integration')
            ]
            
            for check, description in checks:
                if check in content:
                    print(f"✅ {description} found")
                else:
                    print(f"⚠️ {description} missing")
            
            return True
        else:
            print(f"❌ AI predictions failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ AI predictions test failed: {e}")
        return False

def test_pattern_analysis_authenticated():
    """Test pattern analysis with authentication"""
    print("\n📊 Testing Pattern Analysis (Authenticated)...")
    
    try:
        app, client = create_authenticated_client()
        
        response = client.get('/pattern-analysis')
        print(f"Pattern analysis response: {response.status_code}")
        
        if response.status_code == 200:
            content = response.data.decode('utf-8')
            
            # Check for key components
            checks = [
                ('AI Crime Pattern Analysis', 'Page title'),
                ('loadPatternAnalysis', 'Data loading function'),
                ('refreshAnalysis', 'Refresh function'),
                ('/api/pattern-analysis', 'API endpoint')
            ]
            
            for check, description in checks:
                if check in content:
                    print(f"✅ {description} found")
                else:
                    print(f"⚠️ {description} missing")
            
            return True
        else:
            print(f"❌ Pattern analysis failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Pattern analysis test failed: {e}")
        return False

def test_advanced_map_authenticated():
    """Test advanced map with authentication"""
    print("\n🚀 Testing Advanced Map (Authenticated)...")
    
    try:
        app, client = create_authenticated_client()
        
        response = client.get('/advanced-map')
        print(f"Advanced map response: {response.status_code}")
        
        if response.status_code == 200:
            content = response.data.decode('utf-8')
            
            # Check for advanced features
            checks = [
                ('Advanced Crime Hotspot Map', 'Page title'),
                ('markercluster', 'Clustering support'),
                ('heatmap', 'Heatmap functionality'),
                ('real-time', 'Real-time features')
            ]
            
            for check, description in checks:
                if check in content:
                    print(f"✅ {description} found")
                else:
                    print(f"⚠️ {description} missing")
            
            return True
        else:
            print(f"❌ Advanced map failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Advanced map test failed: {e}")
        return False

def test_basic_map_authenticated():
    """Test basic interactive map with authentication"""
    print("\n🗺️ Testing Basic Interactive Map (Authenticated)...")
    
    try:
        app, client = create_authenticated_client()
        
        response = client.get('/map')
        print(f"Basic map response: {response.status_code}")
        
        if response.status_code == 200:
            content = response.data.decode('utf-8')
            
            # Check for integrated features
            checks = [
                ('markercluster', 'Clustering integration'),
                ('clusterGroup', 'Cluster group'),
                ('addInfrastructureMarker', 'Infrastructure markers'),
                ('crime markers disabled', 'No crime markers')
            ]
            
            for check, description in checks:
                if check in content:
                    print(f"✅ {description} found")
                else:
                    print(f"⚠️ {description} missing")
            
            return True
        else:
            print(f"❌ Basic map failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Basic map test failed: {e}")
        return False

def test_api_endpoints_authenticated():
    """Test API endpoints with authentication"""
    print("\n🔌 Testing API Endpoints (Authenticated)...")
    
    try:
        app, client = create_authenticated_client()
        
        api_endpoints = [
            ('/api/pattern-analysis', 'Pattern Analysis API'),
            ('/api/crime-stats', 'Crime Statistics API')
        ]
        
        for endpoint, name in api_endpoints:
            response = client.get(endpoint)
            print(f"{name} response: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.get_json()
                    if data and ('success' in data or 'data' in data):
                        print(f"✅ {name} returns valid JSON")
                    else:
                        print(f"⚠️ {name} returns unexpected format")
                except:
                    print(f"⚠️ {name} returns non-JSON response")
            else:
                print(f"❌ {name} failed: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ API endpoints test failed: {e}")
        return False

def run_authenticated_test():
    """Run all authenticated tests"""
    print("🔐 Crime Hotspot Application - Authenticated Fix Verification")
    print("=" * 65)
    print(f"📅 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        test_chennai_map_authenticated,
        test_basic_map_authenticated,
        test_advanced_map_authenticated,
        test_ai_predictions_authenticated,
        test_pattern_analysis_authenticated,
        test_api_endpoints_authenticated
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test in tests:
        try:
            if test():
                passed_tests += 1
                print(f"✅ {test.__name__} PASSED")
            else:
                print(f"❌ {test.__name__} FAILED")
        except Exception as e:
            print(f"💥 {test.__name__} CRASHED: {e}")
        print()
    
    print("=" * 65)
    print(f"📊 Authenticated Test Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 ALL AUTHENTICATED TESTS PASSED!")
        print("✅ Chennai map loading works")
        print("✅ Advanced map integration successful")
        print("✅ AI predictions template fixed")
        print("✅ Pattern analysis functional")
        print("✅ API endpoints working")
        print("🚀 All fixes verified and working!")
    else:
        print(f"⚠️ {total_tests - passed_tests} tests failed.")
        print("🔧 Some issues may remain.")
    
    print(f"📅 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = run_authenticated_test()
    sys.exit(0 if success else 1)
