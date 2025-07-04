FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 && rm -rf /var/lib/apt/lists/*

COPY server/ /app/server/

COPY src/ /app/

COPY setup.py /app/

RUN pip install --no-cache-dir -r server/requirements.txt

RUN pip install --no-cache-dir -e .

RUN python -m nltk.downloader stopwords wordnet

EXPOSE 5000

CMD ["python", "server/app.py"]

