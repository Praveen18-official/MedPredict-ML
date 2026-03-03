from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return {
        'message': 'Hello from MedPredict API!',
        'status': 'success',
        'version': '1.0.0',
        'port': os.environ.get('PORT', 'not set'),
        'environment': 'production'
    }

@app.route('/health')
def health():
    return {
        'status': 'healthy',
        'message': 'API is working',
        'port': os.environ.get('PORT', 'not set')
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
