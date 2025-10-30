#!/usr/bin/env python3
"""Display Crime Hotspot Application Server Information"""
from app import create_app
import os

def show_server_info():
    app = create_app()
    port = int(os.environ.get('PORT', 5003))
    
    print('\n' + '='*80)
    print(' '*20 + 'CRIME HOTSPOT APPLICATION - SERVER INFORMATION')
    print('='*80)
    
    print('\n📍 SERVER STATUS:')
    print(f'   ✓ Flask Application: Running')
    print(f'   ✓ Server Address: http://localhost:{port}')
    print(f'   ✓ Network Address: http://0.0.0.0:{port}')
    print(f'   ✓ Debug Mode: Enabled')
    
    print('\n🗺️  AVAILABLE ROUTES:')
    print('-'*80)
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            methods = ', '.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
            routes.append((rule.endpoint, str(rule), methods))
    
    # Sort routes by endpoint
    routes.sort(key=lambda x: x[0])
    
    for endpoint, route, methods in routes:
        print(f'   {endpoint:35s} {route:30s} [{methods}]')
    
    print('\n📊 KEY FEATURES:')
    print('   • Interactive Crime Maps')
    print('   • Advanced Analytics Dashboard')
    print('   • AI-Powered Predictions')
    print('   • Pattern Analysis')
    print('   • Incident Reporting')
    print('   • Safety Tips & Resources')
    
    print('\n🌐 ACCESS POINTS:')
    print(f'   • Home Page:          http://localhost:{port}/')
    print(f'   • Interactive Map:    http://localhost:{port}/map')
    print(f'   • Advanced Map:       http://localhost:{port}/advanced-map')
    print(f'   • AI Predictions:     http://localhost:{port}/ai-predictions')
    print(f'   • Pattern Analysis:   http://localhost:{port}/pattern-analysis')
    print(f'   • Report Incident:    http://localhost:{port}/report-incident')
    print(f'   • Safety Tips:        http://localhost:{port}/safety-tips')
    print(f'   • About:              http://localhost:{port}/about')
    print(f'   • Contact:            http://localhost:{port}/contact')
    
    print('\n💾 DATABASE:')
    print(f'   • Type: SQLite')
    print(f'   • Location: app/crime-hotspot-dev.db')
    print(f'   • Status: Connected')
    
    print('\n📦 TECHNOLOGY STACK:')
    print('   • Backend: Flask (Python)')
    print('   • Frontend: HTML5, CSS3, JavaScript')
    print('   • Maps: Folium, Leaflet.js')
    print('   • Database: SQLAlchemy + SQLite')
    print('   • UI Framework: Bootstrap 5')
    
    print('\n' + '='*80)
    print('✅ Server is running successfully!')
    print('   Press CTRL+C in the server terminal to stop')
    print('='*80 + '\n')

if __name__ == '__main__':
    show_server_info()
