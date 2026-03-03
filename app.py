from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import os
import sys

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load model artifacts with error handling
model = None
scaler = None
columns = []

try:
    # Try loading model files
    model_path = os.path.join(os.path.dirname(__file__), "medpredict_model.pkl")
    scaler_path = os.path.join(os.path.dirname(__file__), "scaler.pkl")
    columns_path = os.path.join(os.path.dirname(__file__), "model_columns.pkl")
    
    print(f"Loading model from: {model_path}")
    model = pickle.load(open(model_path, "rb"))
    
    print(f"Loading scaler from: {scaler_path}")
    scaler = pickle.load(open(scaler_path, "rb"))
    
    print(f"Loading columns from: {columns_path}")
    columns = pickle.load(open(columns_path, "rb"))
    
    print("✅ Model, scaler, and columns loaded successfully!")
    print(f"✅ Model type: {type(model)}")
    print(f"✅ Columns: {columns}")
    
except Exception as e:
    print(f"❌ Error loading model files: {e}")
    print(f"❌ Current directory: {os.getcwd()}")
    print(f"❌ Files in directory: {os.listdir('.')}")
    model = None
    scaler = None
    columns = []

@app.route("/")
def home():
    return jsonify({
        "message": "MedPredict ML API",
        "status": "running",
        "model_loaded": model is not None
    })

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500
    
    try:
        data = request.json

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

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None,
        "columns_count": len(columns) if columns else 0
    })

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host="0.0.0.0", port=port)