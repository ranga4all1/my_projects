# Write a script for loading models with pickle and then score this client:
# {"reports": 0, "share": 0.001694, "expenditure": 0.12, "owner": "yes"}

import pickle

def load(filename):
    with open(filename, 'rb') as f_in:
        return pickle.load(f_in)

dv = load('dv.bin')
model = load('model1.bin')

customer = {"reports": 0, "share": 0.001694, "expenditure": 0.12, "owner": "yes"}

X = dv.transform([customer])
y_pred = model.predict_proba(X)[0, 1]

print(y_pred)