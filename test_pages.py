#!/usr/bin/env python3
"""
Test all pages to verify they're working
"""

import requests

def test_pages():
    """Test all application pages"""
    print("🔍 Testing application pages...")
    
    base_url = "http://127.0.0.1:5000"
    
    # Test pages that should work without login
    public_pages = [
        ('/', 'Home Page'),
        ('/auth/login', 'Login Page')
    ]
    
    # Test pages that should redirect to login (302)
    protected_pages = [
        ('/advanced-map', 'Advanced Map'),
        ('/pattern-analysis', 'Pattern Analysis'),
        ('/ai-predictions', 'AI Dashboard')
    ]
    
    print("\n📋 Testing public pages (should return 200):")
    for path, name in public_pages:
        try:
            response = requests.get(f"{base_url}{path}", timeout=10)
            status = "✅ OK" if response.status_code == 200 else f"❌ Error {response.status_code}"
            print(f"  {name}: {status}")
        except Exception as e:
            print(f"  {name}: ❌ Failed - {e}")
    
    print("\n🔐 Testing protected pages (should redirect to login - 302):")
    for path, name in protected_pages:
        try:
            response = requests.get(f"{base_url}{path}", timeout=10, allow_redirects=False)
            if response.status_code == 302:
                print(f"  {name}: ✅ Correctly redirects to login")
            else:
                print(f"  {name}: ❌ Unexpected status {response.status_code}")
        except Exception as e:
            print(f"  {name}: ❌ Failed - {e}")
    
    print("\n🎯 Testing API endpoints:")
    api_endpoints = [
        ('/api/pattern-analysis', 'Pattern Analysis API')
    ]
    
    for path, name in api_endpoints:
        try:
            response = requests.get(f"{base_url}{path}", timeout=10, allow_redirects=False)
            if response.status_code == 302:
                print(f"  {name}: ✅ Correctly requires authentication")
            else:
                print(f"  {name}: ❌ Unexpected status {response.status_code}")
        except Exception as e:
            print(f"  {name}: ❌ Failed - {e}")

if __name__ == "__main__":
    test_pages()
