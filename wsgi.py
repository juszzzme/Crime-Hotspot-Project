from app import create_app

print("🚀 Starting Crime Hotspot Application...")
app = create_app()
print("✅ Flask app created successfully")

if __name__ == "__main__":
    print("🌐 Starting Flask development server...")
    print("📍 Access the application at: http://127.0.0.1:5000")
    print("🔐 Login with: admin@crimesense.com / admin123")
    app.run(debug=True, host='127.0.0.1', port=5000)
