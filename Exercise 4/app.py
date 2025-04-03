# app.py
# Add these imports at the top of app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle
import numpy as np
import os

# Import the model class
from model import SimpleSentimentClassifier

app = Flask(__name__)
CORS(app)  # Enable CORS

# Load the model
model_path = os.environ.get('MODEL_PATH', 'sentiment_model.pkl')

with open(model_path, 'rb') as f:
    model = pickle.load(f)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'model_version': os.environ.get('MODEL_VERSION', '1.0.0')})

@app.route('/predict', methods=['POST'])
def predict():
    # Get data from request
    data = request.json
    
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    # Make prediction
    text = data['text']
    prediction = model.predict([text])[0]
    
    # Map class label to sentiment
    sentiment_map = {0: 'negative', 1: 'neutral', 2: 'positive'}
    sentiment = sentiment_map[prediction]
    
    # Get confidence scores if available
    try:
        confidence_scores = model.predict_proba([text])[0]
        score = float(confidence_scores[prediction])
    except:
        # If predict_proba is not available, use a simple score
        score = 1.0
    
    # Return result
    return jsonify({
        'text': text,
        'sentiment': sentiment,
        'score': score
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)  # Change debug to False