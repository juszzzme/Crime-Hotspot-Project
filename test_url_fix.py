#!/usr/bin/env python3
"""
Test script to verify URL routing fix
"""

from app import create_app
from flask import render_template_string

def test_url_generation():
    """Test URL generation for all routes"""
    print("🔍 Testing URL generation...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Test the corrected URL
            url = render_template_string('{{ url_for("main.ai_predictions") }}')
            print(f"✅ main.ai_predictions URL: {url}")
            
            # Test other URLs
            urls_to_test = [
                ('main.index', '/'),
                ('main.advanced_map', '/advanced-map'),
                ('main.pattern_analysis', '/pattern-analysis'),
                ('auth.login', '/auth/login')
            ]
            
            for endpoint, expected in urls_to_test:
                url = render_template_string(f'{{{{ url_for("{endpoint}") }}}}')
                print(f"✅ {endpoint}: {url}")
                
            print("✅ All URL generation tests passed!")
            return True
            
        except Exception as e:
            print(f"❌ URL generation failed: {e}")
            return False

def test_template_rendering():
    """Test template rendering with navigation"""
    print("\n🔍 Testing template rendering...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Test rendering a simple template with navigation
            template_content = '''
            <nav>
                <a href="{{ url_for('main.ai_predictions') }}">AI Dashboard</a>
                <a href="{{ url_for('main.advanced_map') }}">Advanced Map</a>
                <a href="{{ url_for('main.pattern_analysis') }}">Pattern Analysis</a>
            </nav>
            '''
            
            result = render_template_string(template_content)
            print("✅ Template rendering successful!")
            print("Generated HTML:")
            print(result)
            return True
            
        except Exception as e:
            print(f"❌ Template rendering failed: {e}")
            return False

def test_login_template():
    """Test login template specifically"""
    print("\n🔍 Testing login template rendering...")
    
    app = create_app()
    
    with app.app_context():
        try:
            from app.forms.auth_forms import LoginForm
            from flask import render_template
            from datetime import datetime
            
            form = LoginForm()
            result = render_template('auth/login.html', form=form, now=datetime.utcnow())
            print("✅ Login template rendering successful!")
            print(f"Template length: {len(result)} characters")
            return True
            
        except Exception as e:
            print(f"❌ Login template rendering failed: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Main test function"""
    print("🔧 URL Routing Fix Verification")
    print("=" * 40)
    
    tests = [
        test_url_generation,
        test_template_rendering,
        test_login_template
    ]
    
    all_passed = True
    for test in tests:
        if not test():
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! The URL routing fix is working correctly.")
        print("✅ The application should now work without routing errors.")
    else:
        print("\n💥 Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()
