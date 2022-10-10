# Write Flask code for serving the model

from flask import Flask, request, jsonify
import pickle

def load(filename):
    with open(filename, 'rb') as f_in:
        return pickle.load(f_in)

dv = load('dv.bin')
model = load('model1.bin')


app = Flask('score')

@app.route('/predict', methods=['POST'])
def predict():
    customer = request.get_json()

    X = dv.transform([customer])
    y_pred = model.predict_proba(X)[0, 1]
    score = y_pred >= 0.5

    result = {
        'score_probability': float(y_pred),
        'score': bool(score)
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)