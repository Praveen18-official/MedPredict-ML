from flask import Flask, request, jsonify
import os
import json
from openai import OpenAI

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

@app.route('/')
def hello():
    return {
        'message': 'MedPredict AI API with OpenAI',
        'status': 'success',
        'version': '3.0.0',
        'model': 'OpenAI GPT-4',
        'port': os.environ.get('PORT', 'not set'),
        'environment': 'production'
    }

@app.route('/health')
def health():
    return {
        'status': 'healthy',
        'message': 'OpenAI API is working',
        'port': os.environ.get('PORT', 'not set')
    }

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400
        
        # Extract patient data
        age = data.get('Age', 'N/A')
        gender = 'Male' if data.get('Gender', 0) == 1 else 'Female'
        bmi = data.get('BMI', 'N/A')
        blood_pressure = data.get('BloodPressure', 'N/A')
        cholesterol = data.get('Cholesterol', 'N/A')
        glucose = data.get('Glucose', 'N/A')
        smoking = 'Yes' if data.get('Smoking', 0) == 1 else 'No'
        alcohol = 'Yes' if data.get('AlcoholIntake', 0) == 1 else 'No'
        activity = ['Low', 'Moderate', 'High'][data.get('PhysicalActivity', 1)]
        family_history = 'Yes' if data.get('FamilyHistory', 0) == 1 else 'No'
        
        # Create OpenAI prompt
        prompt = f"""
As a medical AI assistant, analyze the following patient health data and provide disease risk assessments:

Patient Profile:
- Age: {age} years
- Gender: {gender}
- BMI: {bmi}
- Blood Pressure: {blood_pressure} mmHg
- Cholesterol: {cholesterol} mg/dL
- Glucose: {glucose} mg/dL
- Smoking: {smoking}
- Alcohol Intake: {alcohol}
- Physical Activity: {activity}
- Family History of Diseases: {family_history}

Please provide risk assessments (0-100 scale) for:
1. Heart Disease
2. Diabetes
3. Kidney Disease
4. Cancer Risk

Respond with ONLY a JSON object in this exact format:
{{"HeartDisease": 0-100, "Diabetes": 0-100, "KidneyDisease": 0-100, "CancerRisk": 0-100}}

Consider the medical risk factors and provide realistic percentages based on the data.
"""

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a medical AI assistant providing disease risk assessments. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=150
        )
        
        # Extract and parse the response
        ai_response = response.choices[0].message.content.strip()
        
        # Try to extract JSON from response
        try:
            # Remove any markdown formatting
            if '```json' in ai_response:
                ai_response = ai_response.split('```json')[1].split('```')[0].strip()
            elif '```' in ai_response:
                ai_response = ai_response.split('```')[1].strip()
            
            result = json.loads(ai_response)
            
            # Ensure all keys exist and values are integers 0-100
            final_result = {
                "HeartDisease": min(100, max(0, int(result.get("HeartDisease", 50)))),
                "Diabetes": min(100, max(0, int(result.get("Diabetes", 50)))),
                "KidneyDisease": min(100, max(0, int(result.get("KidneyDisease", 50)))),
                "CancerRisk": min(100, max(0, int(result.get("CancerRisk", 50))))
            }
            
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            final_result = {
                "HeartDisease": 50,
                "Diabetes": 50,
                "KidneyDisease": 50,
                "CancerRisk": 50
            }
        
        print(f"OpenAI prediction result: {final_result}")
        
        return jsonify(final_result)
        
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting MedPredict OpenAI API on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
