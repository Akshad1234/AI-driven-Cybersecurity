from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import joblib
import numpy as np
import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Change for production
jwt = JWTManager(app)
CORS(app)

# Load trained model and scaler
model = joblib.load('cybersecurity_model.pkl')
scaler = joblib.load('scaler.pkl')

# User authentication
users = {"admin": "password123"}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username in users and users[username] == password:
        token = create_access_token(identity=username, expires_delta=datetime.timedelta(hours=1))
        return jsonify({"token": token})
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/predict', methods=['POST'])
@jwt_required()
def predict():
    data = request.get_json()
    features = np.array(data['features']).reshape(1, -1)
    scaled_features = scaler.transform(features)
    prediction = model.predict(scaled_features)[0]
    result = "Malicious Activity Detected!" if prediction == 1 else "No Threat Detected"
    return jsonify({"prediction": result})

@app.route('/api/threats', methods=['GET'])
def get_threats():
    # Mock data for dashboard
    threats = [
        {"timestamp": "2024-12-26 10:00", "threat_level": 5},
        {"timestamp": "2024-12-26 10:10", "threat_level": 3},
        {"timestamp": "2024-12-26 10:20", "threat_level": 8},
    ]
    return jsonify(threats)

if __name__ == "__main__":
    app.run(debug=True)
