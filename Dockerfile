FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libgomp1

COPY server/ /app/

COPY tfidf_vectorizer.pkl /app/tfidf_vectorizer.pkl

RUN pip install -r requirements.txt

RUN python -m nltk.downloader stopwords wordnet

EXPOSE 5000

CMD ["python", "app.py"]

# # Stage 1: Build Stage
# FROM python:3.10 AS build

# WORKDIR /app

# RUN apt-get update && apt-get install -y libgomp1

# # Copy the requirements.txt file from the server folder
# COPY server/requirements.txt /app/

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the application code and model files
# COPY server/ /app/
# COPY tfidf_vectorizer.pkl /app/tfidf_vectorizer.pkl

# # Download only the necessary NLTK data
# RUN python -m nltk.downloader stopwords wordnet

# # Stage 2: Final Stage
# FROM python:3.10-slim AS final

# WORKDIR /app

# # Copy only the necessary files from the build stage
# COPY --from=build /app /app

# # Expose the application port
# EXPOSE 5000

# # Set the command to run the application
# CMD ["python", "app.py"]
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "app:app"]
