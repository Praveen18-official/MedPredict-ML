import http.server
import socketserver
import os
import json
import pickle
import pandas as pd

# Load model artifacts
model = None
scaler = None
columns = []

try:
    print("Loading ML model...")
    model = pickle.load(open("medpredict_model.pkl", "rb"))
    scaler = pickle.load(open("scaler.pkl", "rb"))
    columns = pickle.load(open("model_columns.pkl", "rb"))
    print("✅ ML Model loaded successfully!")
    print(f"✅ Model features: {columns}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None
    scaler = None
    columns = []

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            response_data = {
                'message': 'MedPredict ML API is running!',
                'status': 'success',
                'version': '2.0.0',
                'model_loaded': model is not None,
                'port': os.environ.get('PORT', 'not set'),
                'environment': 'production'
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
        elif self.path == '/health':
            response_data = {
                'status': 'healthy',
                'message': 'API is working',
                'model_loaded': model is not None,
                'port': os.environ.get('PORT', 'not set')
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
        elif self.path == '/predict':
            if model is None:
                response_data = {'error': 'Model not loaded'}
                self.send_response(503)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode())
                return
            
            # For POST requests, we need to handle them differently
            # This is a limitation of SimpleHTTPRequestHandler
            response_data = {'error': 'Use POST method for /predict endpoint'}
            self.send_response(405)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/predict':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                print(f"Received prediction request: {data}")
                
                # Convert input to DataFrame
                input_df = pd.DataFrame([data], columns=columns)
                
                # Scale input
                input_scaled = scaler.transform(input_df)
                
                # Predict
                prediction = model.predict(input_scaled)
                
                result = {
                    "HeartDisease": int(prediction[0][0]),
                    "Diabetes": int(prediction[0][1]),
                    "KidneyDisease": int(prediction[0][2]),
                    "CancerRisk": int(prediction[0][3])
                }
                
                print(f"Prediction result: {result}")
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
                
            except Exception as e:
                print(f"Prediction error: {e}")
                response_data = {'error': str(e)}
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode())
        else:
            super().do_POST()

port = int(os.environ.get('PORT', 5000))
print(f"Starting MedPredict ML API on port {port}")
print(f"Model loaded: {model is not None}")

with socketserver.TCPServer(("", port), MyHandler) as httpd:
    httpd.serve_forever()
