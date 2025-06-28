from flask import Flask

app= Flask(__name__)

@app.route('/')

def home():
    
    return '🚨 Cirme hotspot web app is Running'

if __name__ == '__main__':
    app.run(debug=True)