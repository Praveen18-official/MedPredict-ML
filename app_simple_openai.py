from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

# Simple rule-based predictions (no ML model needed)
def get_predictions(data):
    age = int(data.get('Age', 30))
    gender = int(data.get('Gender', 0))
    bmi = float(data.get('BMI', 25))
    blood_pressure = int(data.get('BloodPressure', 120))
    cholesterol = int(data.get('Cholesterol', 200))
    glucose = int(data.get('Glucose', 95))
    smoking = int(data.get('Smoking', 0))
    alcohol = int(data.get('AlcoholIntake', 0))
    activity = int(data.get('PhysicalActivity', 1))
    family_history = int(data.get('FamilyHistory', 0))
    
    # Calculate risk scores based on medical guidelines
    heart_risk = 0
    diabetes_risk = 0
    kidney_risk = 0
    cancer_risk = 0
    
    # Heart Disease Risk Factors
    if age > 45: heart_risk += 20
    if blood_pressure > 140: heart_risk += 25
    if cholesterol > 240: heart_risk += 20
    if smoking == 1: heart_risk += 30
    if family_history == 1: heart_risk += 15
    if bmi > 30: heart_risk += 15
    
    # Diabetes Risk Factors
    if age > 40: diabetes_risk += 15
    if glucose > 125: diabetes_risk += 35
    if bmi > 25: diabetes_risk += 20
    if family_history == 1: diabetes_risk += 20
    if activity == 0: diabetes_risk += 15
    
    # Kidney Disease Risk Factors
    if blood_pressure > 130: kidney_risk += 25
    if glucose > 130: kidney_risk += 20
    if age > 60: kidney_risk += 20
    if family_history == 1: kidney_risk += 15
    
    # Cancer Risk Factors
    if age > 50: cancer_risk += 25
    if smoking == 1: cancer_risk += 30
    if alcohol == 1: cancer_risk += 20
    if family_history == 1: cancer_risk += 25
    
    # Normalize to 0-100 scale
    heart_risk = min(100, heart_risk)
    diabetes_risk = min(100, diabetes_risk)
    kidney_risk = min(100, kidney_risk)
    cancer_risk = min(100, cancer_risk)
    
    return {
        "HeartDisease": heart_risk,
        "Diabetes": diabetes_risk,
        "KidneyDisease": kidney_risk,
        "CancerRisk": cancer_risk
    }

@app.route('/')
def hello():
    return {
        'message': 'MedPredict AI API - Rule-Based Predictions',
        'status': 'success',
        'version': '3.1.0',
        'model': 'Medical Risk Assessment Rules',
        'port': os.environ.get('PORT', 'not set'),
        'environment': 'production'
    }

@app.route('/health')
def health():
    return {
        'status': 'healthy',
        'message': 'Rule-based prediction system is working',
        'port': os.environ.get('PORT', 'not set')
    }

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400
        
        print(f"Received prediction request: {data}")
        
        # Get rule-based predictions
        result = get_predictions(data)
        
        print(f"Rule-based prediction result: {result}")
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting MedPredict Rule-Based API on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
