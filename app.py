from flask import Flask, render_template,request

import re
import pandas as pd
import joblib
import json
import requests
app = Flask(__name__)

modelpath = 'models/logistic.pkl'
cvpath = 'models/countvector.pkl'
model =  joblib.load(modelpath)
countvector = joblib.load(cvpath)

@app.route('/', methods=['post','get'])
def index():
    
    input = ''
    predictions = ''
    if request.method == 'POST':
        input = request.form.get('input')
        processed_text = preprocessing(input)  
        input_vec = countvector.transform([processed_text]) 
        predictions = predict(input_vec)

        
        
    return render_template('index.html',result=predictions,text=input)

def predict( X):
    predictions = model.predict(X)
    return predictions


def preprocessing(text):
  text = text.lower()
  emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
  url_pattern = re.compile(r'https?://\S+|www\.\S+')
  html_pattern = re.compile('<.*?>')
  text = emoji_pattern.sub(r'', text)
  text = url_pattern.sub(r'', text)
  text = html_pattern.sub(r'', text)
  text = re.sub(r"[^\w\d'\s]+", '', text)

  return text


if __name__ == '__main__':
    app.run()
