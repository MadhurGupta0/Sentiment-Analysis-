from flask import Flask, request,jsonify
from textblob import TextBlob
from flask_cors import CORS
from waitress import serve


import pandas as pd

app = Flask(__name__)
CORS(app)

def get_sentiment_scores(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    return sentiment

def process_file(file):
    if file.filename.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.filename.endswith('.xlsx'):
        df = pd.read_excel(file, engine='openpyxl')
    else:
        return None, 'Unsupported file format. Please upload CSV or XLSX.'

    if 'Review' in df.columns:
        return df['Review'].tolist(), None
    elif 'review' in df.columns:
        return df['review'].tolist(), None

    return None, 'No review column found in the file.'

@app.route('/analyze', methods=['POST'])
def analyze_reviews():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    reviews, error = process_file(file)

    if error:
        return jsonify({'error': error}), 400

    sentiments = {'positive': 0, 'negative': 0, 'neutral': 0}

    for review in reviews:
        sentiment_result = get_sentiment_scores(review)
        if sentiment_result >0:
            sentiments['positive'] += 1
        elif sentiment_result < 0:
            sentiments['negative'] += 1
        else:
            sentiments['neutral'] += 1


    return jsonify(sentiments)

if __name__ == '__main__':
    serve(app, host="127.0.0.1", port=5000)

