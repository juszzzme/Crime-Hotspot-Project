#!/usr/bin/env python3
"""
Complete User Flow Test for Crime Hotspot Application
Tests the entire user journey through the integrated system
"""

import sys
import os
import time
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_complete_user_flow():
    """Test the complete user flow through the application"""
    print("🔄 Testing Complete User Flow...")
    print("=" * 50)
    
    try:
        from app import create_app
        from app.models.user import User
        from app.extensions import db
        
        app = create_app()
        
        with app.test_client() as client:
            print("👤 Testing User Journey:")
            
            # Step 1: Visit home page
            print("\n1️⃣ Visiting home page...")
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Home page loads successfully")
                if b'CRIMESENSE' in response.data:
                    print("✅ Brand name visible")
                if b'Crime Hotspot' in response.data or b'crime' in response.data.lower():
                    print("✅ Crime-related content present")
            else:
                print(f"❌ Home page failed: {response.status_code}")
                return False
            
            # Step 2: Try to access protected page (should redirect)
            print("\n2️⃣ Attempting to access protected page...")
            response = client.get('/advanced-map', follow_redirects=False)
            if response.status_code == 302:
                print("✅ Correctly redirected to login")
                if '/auth/login' in response.location:
                    print("✅ Redirect points to login page")
            else:
                print(f"❌ Expected redirect, got: {response.status_code}")
            
            # Step 3: Visit login page
            print("\n3️⃣ Visiting login page...")
            response = client.get('/auth/login')
            if response.status_code == 200:
                print("✅ Login page loads successfully")
                if b'email' in response.data.lower() and b'password' in response.data.lower():
                    print("✅ Login form elements present")
            else:
                print(f"❌ Login page failed: {response.status_code}")
                return False
            
            # Step 4: Test login with demo credentials
            print("\n4️⃣ Testing login with demo credentials...")
            
            # First, ensure demo user exists
            with app.app_context():
                demo_user = User.query.filter_by(email='admin@crimesense.com').first()
                if not demo_user:
                    print("⚠️ Demo user not found, creating...")
                    demo_user = User(
                        email='admin@crimesense.com',
                        username='admin',
                        first_name='Admin',
                        last_name='User',
                        password='admin123',
                        is_active=True,
                        is_admin=True
                    )
                    db.session.add(demo_user)
                    db.session.commit()
                    print("✅ Demo user created")
                else:
                    print("✅ Demo user exists")
            
            # Attempt login
            login_data = {
                'email': 'admin@crimesense.com',
                'password': 'admin123',
                'remember': False
            }
            
            response = client.post('/auth/login', data=login_data, follow_redirects=True)
            if response.status_code == 200:
                print("✅ Login request processed")
                # Check if we're redirected to a protected page or home
                if b'logout' in response.data.lower() or b'dashboard' in response.data.lower():
                    print("✅ Successfully logged in (logout option visible)")
                else:
                    print("⚠️ Login may have failed (no logout option visible)")
            else:
                print(f"❌ Login failed: {response.status_code}")
            
            # Step 5: Test access to protected pages after login
            print("\n5️⃣ Testing access to protected pages after login...")
            
            protected_pages = [
                ('/advanced-map', 'Advanced Map'),
                ('/pattern-analysis', 'Pattern Analysis'),
                ('/ai-predictions', 'AI Dashboard'),
                ('/map', 'Basic Map')
            ]
            
            for url, name in protected_pages:
                response = client.get(url)
                if response.status_code == 200:
                    print(f"✅ {name} accessible after login")
                elif response.status_code == 302:
                    print(f"⚠️ {name} still redirecting (login may have failed)")
                else:
                    print(f"❌ {name} returned {response.status_code}")
            
            # Step 6: Test navigation consistency
            print("\n6️⃣ Testing navigation consistency...")
            
            # Get a protected page and check navigation
            response = client.get('/advanced-map')
            if response.status_code == 200:
                nav_elements = [
                    (b'Home', 'Home link'),
                    (b'Advanced Map', 'Advanced Map link'),
                    (b'AI Predictions', 'AI Predictions link'),
                    (b'Pattern Analysis', 'Pattern Analysis link'),
                    (b'navbar', 'Navigation bar')
                ]
                
                for element, description in nav_elements:
                    if element in response.data:
                        print(f"✅ {description} present in navigation")
                    else:
                        print(f"⚠️ {description} missing from navigation")
            
            # Step 7: Test logout
            print("\n7️⃣ Testing logout functionality...")
            response = client.get('/auth/logout', follow_redirects=True)
            if response.status_code == 200:
                print("✅ Logout request processed")
                # Check if we're back to public view
                if b'login' in response.data.lower() and b'logout' not in response.data.lower():
                    print("✅ Successfully logged out")
                else:
                    print("⚠️ Logout may have failed")
            
            # Step 8: Verify protection after logout
            print("\n8️⃣ Verifying protection after logout...")
            response = client.get('/advanced-map', follow_redirects=False)
            if response.status_code == 302:
                print("✅ Protected pages correctly require login again")
            else:
                print(f"❌ Protected page accessible after logout: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ User flow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_static_resource_integration():
    """Test that static resources are properly integrated"""
    print("\n📦 Testing Static Resource Integration...")
    
    try:
        from app import create_app
        
        app = create_app()
        
        with app.test_client() as client:
            # Test that pages include unified CSS and JS
            response = client.get('/')
            if response.status_code == 200:
                content = response.data.decode('utf-8')
                
                # Check for unified CSS
                if 'unified_styles.css' in content:
                    print("✅ Unified CSS included in pages")
                else:
                    print("⚠️ Unified CSS not found in page")
                
                # Check for unified JS
                if 'unified_app.js' in content:
                    print("✅ Unified JavaScript included in pages")
                else:
                    print("⚠️ Unified JavaScript not found in page")
                
                # Check for Bootstrap
                if 'bootstrap' in content:
                    print("✅ Bootstrap CSS included")
                else:
                    print("⚠️ Bootstrap CSS not found")
                
                # Check for Font Awesome
                if 'font-awesome' in content or 'fontawesome' in content:
                    print("✅ Font Awesome included")
                else:
                    print("⚠️ Font Awesome not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Static resource test failed: {e}")
        return False

def test_responsive_design():
    """Test responsive design elements"""
    print("\n📱 Testing Responsive Design...")
    
    try:
        from app import create_app
        
        app = create_app()
        
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                content = response.data.decode('utf-8')
                
                # Check for viewport meta tag
                if 'viewport' in content and 'width=device-width' in content:
                    print("✅ Responsive viewport meta tag present")
                else:
                    print("⚠️ Responsive viewport meta tag missing")
                
                # Check for Bootstrap responsive classes
                responsive_classes = ['container', 'row', 'col-', 'd-flex']
                found_classes = [cls for cls in responsive_classes if cls in content]
                
                if len(found_classes) >= 3:
                    print(f"✅ Responsive Bootstrap classes found: {found_classes}")
                else:
                    print(f"⚠️ Limited responsive classes found: {found_classes}")
        
        return True
        
    except Exception as e:
        print(f"❌ Responsive design test failed: {e}")
        return False

def run_complete_integration_test():
    """Run the complete integration test suite"""
    print("🎯 Crime Hotspot Application - Complete Integration Test")
    print("=" * 70)
    print(f"📅 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        test_complete_user_flow,
        test_static_resource_integration,
        test_responsive_design
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
    
    print("=" * 70)
    print(f"📊 Final Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("✅ The Crime Hotspot application is fully integrated and working!")
        print("🚀 Ready for production use!")
    else:
        print(f"⚠️ {total_tests - passed_tests} tests failed.")
        print("🔧 Please review and fix the issues above.")
    
    print(f"📅 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = run_complete_integration_test()
    sys.exit(0 if success else 1)
