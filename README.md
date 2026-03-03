# MedPredict ML API

## Overview
This is the machine learning API for MedPredict - an AI-powered medical disease prediction platform.

## Features
- Disease risk prediction for Heart Disease, Diabetes, Kidney Disease, and Cancer
- RESTful API endpoints
- CORS enabled for frontend integration
- Pre-trained model with feature scaling

## API Endpoints

### GET `/`
Returns API status and model information.

### POST `/predict`
Predicts disease risk based on patient data.

**Request Body:**
```json
{
  "Age": 45,
  "Gender": 1,
  "BMI": 25.5,
  "BloodPressure": 120,
  "Cholesterol": 200,
  "Glucose": 95,
  "Smoking": 0,
  "AlcoholIntake": 1,
  "PhysicalActivity": 2,
  "FamilyHistory": 0
}
```

**Response:**
```json
{
  "HeartDisease": 0,
  "Diabetes": 1,
  "KidneyDisease": 0,
  "CancerRisk": 0
}
```

### GET `/health`
Health check endpoint.

## Model Features
- **Age**: Patient age (years)
- **Gender**: 0 = Female, 1 = Male
- **BMI**: Body Mass Index
- **BloodPressure**: Systolic blood pressure (mmHg)
- **Cholesterol**: Total cholesterol (mg/dL)
- **Glucose**: Blood glucose level (mg/dL)
- **Smoking**: 0 = Non-smoker, 1 = Smoker
- **AlcoholIntake**: 0 = None, 1 = Moderate, 2 = Heavy
- **PhysicalActivity**: 0 = Low, 1 = Moderate, 2 = High
- **FamilyHistory**: 0 = No, 1 = Yes

## Deployment

This API is designed to be deployed on Render.com.

### Environment Variables
- `PORT` (default: 5000)

### Build Command
```bash
pip install -r requirements.txt
```

### Start Command
```bash
gunicorn app:app --bind 0.0.0.0:$PORT
```

## Development

### Local Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

The API will be available at `http://localhost:5000`

## Model Information
- **Algorithm**: Random Forest Classifier
- **Training Data**: Medical dataset with 10 features
- **Output**: Binary predictions (0 = Low Risk, 1 = High Risk)
- **Accuracy**: ~85% (varies by disease)

## License
© 2024 MedPredict. All rights reserved.
