from flask import Flask, render_template, request
import numpy as np
import pickle
import os

app = Flask(__name__)

# Load the pre-trained model and the scaler
model_path = os.getenv('MODEL_PATH', 'random_forest_model.pkl')
scaler_path = os.getenv('SCALER_PATH', 'scaler.pkl')

model = pickle.load(open(model_path, 'rb'))
scaler = pickle.load(open(scaler_path, 'rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract form data
        age = float(request.form.get('age'))
        sex = request.form.get('sex')
        education = float(request.form.get('education'))
        memory_score = float(request.form.get('memory_score'))
        language_score = float(request.form.get('language_score'))
        visual_score = float(request.form.get('visual_score'))

        # Additional fields for the 6 more features
        executive_score = float(request.form.get('executive_score'))
        attention_score = float(request.form.get('attention_score'))
        orientation_score = float(request.form.get('orientation_score'))
        abstract_thinking = float(request.form.get('abstract_thinking'))
        calculation_ability = float(request.form.get('calculation_ability'))
        judgement_score = float(request.form.get('judgement_score'))

        # Option 1: If you don't need encoding, map 'sex' to numeric directly
        sex_encoded = 1 if sex == 'M' else 0  # Use 1 for Male, 0 for Female

        # Prepare the feature array for prediction
        features = np.array([[age, sex_encoded, education, memory_score, language_score, visual_score,
                              executive_score, attention_score, orientation_score, abstract_thinking,
                              calculation_ability, judgement_score]])

        # Scale the features using the same scaler from training
        features_scaled = scaler.transform(features)

        # Make prediction using the trained model
        prediction = model.predict(features_scaled)[0]

        # Render the result back to the page
        return render_template('index.html', prediction=prediction)

    except Exception as e:
        # Handle any errors and display them on the page
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
