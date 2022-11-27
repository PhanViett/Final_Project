import numpy as np
import pickle
from flask import Flask, request, render_template

# Load ML model
model = pickle.load(open('model.pkl', 'rb'))

app = Flask(__name__)


# Bind home function to URL
@app.route('/')
def home():
    return render_template('heart-disease.html')


# Bind predict function to URL
@app.route('/predict', methods=['POST'])
def predict():
    # Put all form entries values in a list
    features = [float(i) for i in request.form.values()]
    # Convert features to array
    array_features = [np.array(features)]
    # Predict features
    prediction = model.predict(array_features)

    output = prediction

    # Check the output values and retrive the result with html tag based on the value
    if output == 1:
        return render_template('heart-disease.html',
                               result='BAN KHONG CO NGUY CO BI BENH TIM!NHO GIU GIN SUC KHOE BAN NHE ')
    else:
        return render_template('heart-disease.html',
                               result='BAN SE BI BENH TIM DAY! NEN TAP THE DUC DEU DAN DI NHA')


if __name__ == '__main__':
    # Run the application
    app.run()


