from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load model artifacts
try:
    model = pickle.load(open("medpredict_model.pkl", "rb"))
    scaler = pickle.load(open("scaler.pkl", "rb"))
    columns = pickle.load(open("model_columns.pkl", "rb"))
    print("Model, scaler, and columns loaded successfully!")
except FileNotFoundError as e:
    print(f"Error loading model files: {e}")
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