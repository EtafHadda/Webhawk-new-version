# About: api.py
# Author: walid.daboubi@gmail.com
# Version: 1.3 - 2021/11/02

# To be launched as the following
# python3 -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
from utilities import *
from fastapi import FastAPI
from pydantic import BaseModel

class HttpLogQueryModel(BaseModel):
    http_log_line : str

app = FastAPI()

@app.post('/predict')

def predict(data: HttpLogQueryModel):
    data = data.dict()
    url,encoded = encode_single_log_line(data['http_log_line'])
    model = pickle.load(open(MODEL, 'rb'))
    formatte_encoded = []
    for feature in FEATURES:
        formatte_encoded.append(encoded[feature])
    prediction = int(model.predict([formatte_encoded])[0])
    proba = model.predict_proba([formatte_encoded])[0][prediction]
    return {
        'prediction': str(prediction),
        'proba':str(proba),
        'log_line':data['http_log_line']
    }