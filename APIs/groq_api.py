from flask import Flask, request, jsonify
import pandas as pd
from groq import Groq
from flask_cors import CORS
from waitress import serve

app = Flask(__name__)
CORS(app)
GROQ_API_KEY = "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"


def analyze_sentiment(review):

    client = Groq( api_key=GROQ_API_KEY,)
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are an expert linguist who is good at classifying customer review sentiments into Positive(label=1),Neutral(label=0) and Negative(label=-1).\nCustomer reviews are provided between three backticks.\nIn your output, only return 0, 1,-1 according to the centiment\n\n"
            },
            {
                "role": "user",
                "content": f'{review}'
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
    )
    sentiment = completion.choices[0].message.content
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
        sentiment_result = analyze_sentiment(review)
        if sentiment_result == "1":
            sentiments['positive'] += 1
        elif sentiment_result == "-1":
            sentiments['negative'] += 1
        else:
            sentiments['neutral'] += 1


    return jsonify(sentiments)




if __name__ == "__main__":
    serve(app, host="127.0.0.1", port=5000)

