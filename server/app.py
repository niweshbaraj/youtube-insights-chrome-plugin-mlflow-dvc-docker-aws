# app.py

import os
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend before importing pyplot

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flasgger import Swagger
import io
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import mlflow
import numpy as np
import joblib
import pickle
import re
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from mlflow.tracking import MlflowClient
import matplotlib.dates as mdates

app = Flask(__name__)

CORS(app)  # Enable CORS for all routes

swagger_config = {
    "headers": [],
    "title": "YouTube Insights Chrome Plugin API",
    "version": "1.0",
    "openapi": "3.0.2",
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs"
}

swagger = Swagger(app, config=swagger_config)


# Set your remote tracking URI - AWS EC2 MLFlow server
# Make sure to replace with your actual MLFlow server URI
# mlflow.set_tracking_uri("http://ec2-13-127-25-124.ap-south-1.compute.amazonaws.com:5000/")

# Set up DagsHub credentials for MLflow tracking
dagshub_token = os.getenv("DAGSHUB_PAT")

if not dagshub_token:
    raise EnvironmentError("DAGSHUB_PAT environment variable is not set")

os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

dagshub_url = "https://dagshub.com"
repo_owner = "niweshbaraj"
repo_name = "youtube-insights-chrome-plugin-mlflow-dvc-docker-aws"


# Load the model and vectorizer from the model registry and local storage
def load_model(model_name, stage="Production"):

    # Set up MLflow tracking URI
    mlflow.set_tracking_uri(f'{dagshub_url}/{repo_owner}/{repo_name}.mlflow')

    # Load the model from the MLflow Model Registry
    client = MlflowClient()

    latest = client.get_latest_versions(model_name, stages=[stage])
    if not latest:
        raise RuntimeError(f"No model for '{model_name}' in stage '{stage}'")
    
    model_version = latest[0].version
    model_uri = f"models:/{model_name}/{model_version}"
    print(f"📦 Loading model {model_uri}", flush=True)
    model = mlflow.pyfunc.load_model(model_uri)
    # print(model.metadata.signature)
    return model, model_version

# Initialize the model
model, model_version = load_model("yt_chrome_plugin_model_pipeline", "Production")  # Update paths and versions as needed


@app.route('/')
def home():
    """
    Home endpoint
    ---
    tags:
      - Health Check
    responses:
      200:
        description: Welcome
        content:
          text/plain:
            example: Welcome to our flask api
    """
    return "Welcome to our flask api"


@app.route('/model_version')
def get_model_version():
    """
    Get Current Model Version
    ---
    tags:
      - Model Info
    responses:
        200:
            description: Successfully retrieved model version
            content:
                application/json:
                    example:
                        model_version: "15"
    """
    return jsonify({"model_version": model_version})


# Define the preprocessing function
def preprocess_comment(comment):
    """Apply preprocessing transformations to a comment."""
    try:
        # Convert to lowercase
        comment = comment.lower()

        # Remove trailing and leading whitespaces
        comment = comment.strip()

        # Remove newline characters
        comment = re.sub(r'\n', ' ', comment)

        # Remove non-alphanumeric characters, except punctuation
        comment = re.sub(r'[^A-Za-z0-9\s!?.,]', '', comment)

        # Remove stopwords but retain important ones for sentiment analysis
        stop_words = set(stopwords.words('english')) - {'not', 'but', 'however', 'no', 'yet'}
        comment = ' '.join([word for word in comment.split() if word not in stop_words])

        # Lemmatize the words
        lemmatizer = WordNetLemmatizer()
        comment = ' '.join([lemmatizer.lemmatize(word) for word in comment.split()])

        return comment
    except Exception as e:
        print(f"Error in preprocessing comment: {e}")
        return comment


@app.route('/predict_with_timestamps', methods=['POST'])
def predict_with_timestamps():
    """
    Predict sentiment with timestamps.
    ---
    tags:
      - Sentiment
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              comments:
                type: array
                items:
                  type: object
                  properties:
                    text:
                      type: string
                    timestamp:
                      type: string
                example:
                  - text: "Great!"
                    timestamp: "2025-07-04T10:00:00"
                  - text: "Horrible"
                    timestamp: "2025-07-04T11:00:00"
    responses:
      200:
        description: With timestamps
        content:
          application/json:
            example:
              - comment: "Great!"
                sentiment: "1"
                timestamp: "2025-07-04T10:00:00"
    """
    data = request.json
    comments_data = data.get('comments')
    
    if not comments_data:
        return jsonify({"error": "No comments provided"}), 400

    try:
        comments = [item['text'] for item in comments_data]
        timestamps = [item['timestamp'] for item in comments_data]

        # Preprocess each comment before vectorizing
        preprocessed_comments = [preprocess_comment(comment) for comment in comments]
        
        input_df = pd.DataFrame({'clean_comment': preprocessed_comments})
        
        # Make predictions
        predictions = model.predict(input_df).tolist()  # Convert to list

        # Convert predictions to strings for consistency
        predictions = [str(pred) for pred in predictions]
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500
    
    # Return the response with original comments, predicted sentiments, and timestamps
    response = [{"comment": comment, "sentiment": sentiment, "timestamp": timestamp} for comment, sentiment, timestamp in zip(comments, predictions, timestamps)]
    return jsonify(response)


@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict sentiment of comments.
    ---
    tags:
      - Sentiment
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              comments:
                type: array
                items:
                  type: string
                example: ["This video is great!", "I hate this video."]
    responses:
      200:
        description: Sentiment results
        content:
          application/json:
            example:
              - comment: "This video is great!"
                sentiment: "1"
              - comment: "I hate this video."
                sentiment: "-1"
    """
    data = request.json
    comments = data.get('comments')
    
    if not comments:
        return jsonify({"error": "No comments provided"}), 400

    try:
        # Preprocess each comment before vectorizing
        preprocessed_comments = [preprocess_comment(comment) for comment in comments]
        
        input_df = pd.DataFrame({'clean_comment': preprocessed_comments})

        # Make predictions
        predictions = model.predict(input_df).tolist()  # Convert to list

         ## Debugging
        print("COMMENTS:", comments)
        print("PREPROCESSED:", preprocessed_comments)
        print("DataFrame passed to model:")
        print(input_df)
        print("Predictions:", predictions)
        
        # Convert predictions to strings for consistency
        predictions = [str(pred) for pred in predictions]
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500
    
    # Return the response with original comments and predicted sentiments
    # print("Predictions:", predictions)
    response = [{"comment": comment, "sentiment": sentiment} for comment, sentiment in zip(comments, predictions)]
    return jsonify(response)


@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    """
    Generate pie chart from sentiment counts.
    ---
    tags:
      - Visualization
    requestBody:
      required: true
      content:
        application/json:
          example:
            sentiment_counts: {"1": 4, "0": 3, "-1": 1}
    responses:
      200:
        description: PNG pie chart
        content:
          image/png:
            schema:
              type: string
              format: binary
    """
    try:
        data = request.get_json()
        sentiment_counts = data.get('sentiment_counts')
        
        if not sentiment_counts:
            return jsonify({"error": "No sentiment counts provided"}), 400

        # Prepare data for the pie chart
        labels = ['Positive', 'Neutral', 'Negative']
        sizes = [
            int(sentiment_counts.get('1', 0)),
            int(sentiment_counts.get('0', 0)),
            int(sentiment_counts.get('-1', 0))
        ]
        if sum(sizes) == 0:
            raise ValueError("Sentiment counts sum to zero")
        
        colors = ['#36A2EB', '#C9CBCF', '#FF6384']  # Blue, Gray, Red

        # Generate the pie chart
        plt.figure(figsize=(6, 6))
        plt.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=140,
            textprops={'color': 'w'}
        )
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Save the chart to a BytesIO object
        img_io = io.BytesIO()
        plt.savefig(img_io, format='PNG', transparent=True)
        img_io.seek(0)
        plt.close()

        # Return the image as a response
        return send_file(img_io, mimetype='image/png')
    except Exception as e:
        app.logger.error(f"Error in /generate_chart: {e}")
        return jsonify({"error": f"Chart generation failed: {str(e)}"}), 500
    

@app.route('/generate_wordcloud', methods=['POST'])
def generate_wordcloud():
    """
    Generate word cloud from comments.
    ---
    tags:
      - Visualization
    requestBody:
      required: true
      content:
        application/json:
          example:
            comments: ["Good job", "Great content"]
    responses:
      200:
        description: PNG word cloud
        content:
          image/png:
            schema:
              type: string
              format: binary
    """
    try:
        data = request.get_json()
        comments = data.get('comments')

        if not comments:
            return jsonify({"error": "No comments provided"}), 400

        # Preprocess comments
        preprocessed_comments = [preprocess_comment(comment) for comment in comments]

        # Combine all comments into a single string
        text = ' '.join(preprocessed_comments)

        # Generate the word cloud
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='black',
            colormap='Blues',
            stopwords=set(stopwords.words('english')),
            collocations=False
        ).generate(text)

        # Save the word cloud to a BytesIO object
        img_io = io.BytesIO()
        wordcloud.to_image().save(img_io, format='PNG')
        img_io.seek(0)

        # Return the image as a response
        return send_file(img_io, mimetype='image/png')
    except Exception as e:
        app.logger.error(f"Error in /generate_wordcloud: {e}")
        return jsonify({"error": f"Word cloud generation failed: {str(e)}"}), 500
    

@app.route('/generate_trend_graph', methods=['POST'])
def generate_trend_graph():
    try:
        data = request.get_json()
        sentiment_data = data.get('sentiment_data')

        if not sentiment_data:
            return jsonify({"error": "No sentiment data provided"}), 400

        # Convert sentiment_data to DataFrame
        df = pd.DataFrame(sentiment_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Set the timestamp as the index
        df.set_index('timestamp', inplace=True)

        # Ensure the 'sentiment' column is numeric
        df['sentiment'] = df['sentiment'].astype(int)

        # Map sentiment values to labels
        sentiment_labels = {-1: 'Negative', 0: 'Neutral', 1: 'Positive'}

        # Resample the data over monthly intervals and count sentiments
        monthly_counts = df.resample('M')['sentiment'].value_counts().unstack(fill_value=0)

        # Calculate total counts per month
        monthly_totals = monthly_counts.sum(axis=1)

        # Calculate percentages
        monthly_percentages = (monthly_counts.T / monthly_totals).T * 100

        # Ensure all sentiment columns are present
        for sentiment_value in [-1, 0, 1]:
            if sentiment_value not in monthly_percentages.columns:
                monthly_percentages[sentiment_value] = 0

        # Sort columns by sentiment value
        monthly_percentages = monthly_percentages[[-1, 0, 1]]

        # Plotting
        plt.figure(figsize=(12, 6))

        colors = {
            -1: 'red',     # Negative sentiment
            0: 'gray',     # Neutral sentiment
            1: 'green'     # Positive sentiment
        }

        for sentiment_value in [-1, 0, 1]:
            plt.plot(
                monthly_percentages.index,
                monthly_percentages[sentiment_value],
                marker='o',
                linestyle='-',
                label=sentiment_labels[sentiment_value],
                color=colors[sentiment_value]
            )

        plt.title('Monthly Sentiment Percentage Over Time')
        plt.xlabel('Month')
        plt.ylabel('Percentage of Comments (%)')
        plt.grid(True)
        plt.xticks(rotation=45)

        # Format the x-axis dates
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=12))

        plt.legend()
        plt.tight_layout()

        # Save the trend graph to a BytesIO object
        img_io = io.BytesIO()
        plt.savefig(img_io, format='PNG')
        img_io.seek(0)
        plt.close()

        # Return the image as a response
        return send_file(img_io, mimetype='image/png')
    except Exception as e:
        app.logger.error(f"Error in /generate_trend_graph: {e}")
        return jsonify({"error": f"Trend graph generation failed: {str(e)}"}), 500
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)