# 🔍 YouTube Insights Chrome Plugin

This Chrome extension analyzes YouTube comments using an AI-powered sentiment analysis model. It connects to a locally (web) running backend and uses the YouTube Data API to fetch video comments.

---

## 🚀 Features

- Extracts comments from any YouTube video
- Sends comments to a local (web) API for analysis
- Visualizes sentiment and keyword patterns

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/niweshbaraj/yt-insights-chrome-plugin.git
cd yt-insights-chrome-plugin
```

### 2. Run the Backend API Locally

- Create a Virtual Environment

```bash
conda create -n yt-insights-ch-plugin python=3.8
conda activate yt-insights-ch-plugin
```
- Install Dependencies

```bash
pip install -r requirements.txt
```
- Run the backend app

```bash
python server/app.py
```

- Your API should now be running at: http://localhost:5000

### 3. Set Up the Chrome Plugin

- 1. Open Chrome and navigate to: chrome://extensions/

- 2. Enable Developer mode (top right).

- 3. Click Load unpacked.

- 4. Select the client/ directory from this repo.

### 4. Obtain and Configure Your YouTube API Key

The plugin uses the YouTube Data API v3 to fetch comments.

🔐 Steps to Get an API Key from Google Cloud:

- 1. Go to https://console.cloud.google.com/

- 2. Sign in and create a new project (or select an existing one).

- 3. In the left menu, go to APIs & Services > Library.

- 4. Search for YouTube Data API v3 and click Enable.

- 5. Now go to APIs & Services > Credentials.

- 6. Click Create Credentials > API Key.

- 7. Copy the generated API key.

🔧 Add API Key to Extension

1. In client/popup.js or config.js (wherever you're keeping config):

```js
const YT_API_KEY = "YOUR_API_KEY_HERE";
```

2. Replace "YOUR_API_KEY_HERE" with your actual key.

- 🛡️ Tip: Do not publish your API key in public repositories.


🧪 Testing the Plugin

1. Go to any YouTube video.

2. Click the Chrome extension icon.

3. The plugin will:

    - Fetch comments using the YouTube API

    - Send them to the local Flask backend

    - Display sentiment predictions