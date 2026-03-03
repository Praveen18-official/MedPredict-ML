from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({
        "message": "MedPredict ML API - Simple Version",
        "status": "running",
        "version": "1.0.0"
    })

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        
        # Simple mock prediction for testing
        result = {
            "HeartDisease": 0,
            "Diabetes": 1,
            "KidneyDisease": 0,
            "CancerRisk": 0,
            "message": "Mock prediction - model loading disabled for testing"
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "message": "Simple API working"
    })

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
