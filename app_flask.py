from flask import Flask, request, jsonify
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

app = Flask(__name__)

@app.route('/')
def hello():
    return {
        'message': 'MedPredict ML API is running!',
        'status': 'success',
        'version': '2.0.0',
        'model_loaded': model is not None,
        'port': os.environ.get('PORT', 'not set'),
        'environment': 'production'
    }

@app.route('/health')
def health():
    return {
        'status': 'healthy',
        'message': 'API is working',
        'model_loaded': model is not None,
        'port': os.environ.get('PORT', 'not set')
    }

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 503
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400
        
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
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting MedPredict ML API on port {port}")
    print(f"Model loaded: {model is not None}")
    app.run(host='0.0.0.0', port=port, debug=False)
