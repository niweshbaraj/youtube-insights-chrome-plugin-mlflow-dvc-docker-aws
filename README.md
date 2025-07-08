**Backend URL** : [http://ec2-13-201-230-148.ap-south-1.compute.amazonaws.com/](http://ec2-13-201-230-148.ap-south-1.compute.amazonaws.com/)

**API Doc** : [http://ec2-13-201-230-148.ap-south-1.compute.amazonaws.com/docs](http://ec2-13-201-230-148.ap-south-1.compute.amazonaws.com/docs)

# 🎬 Youtube Insights Chrome Plugin

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

A Chrome extension that gives you instant insights on YouTube videos by analyzing their comments using an end-to-end machine learning pipeline.

Built with modern MLOps practices, the application integrates:

- ⚙️ **MLFlow** for experiment & model tracking & registry/deployment
- 🧪 **DVC** for data versioning and pipeline
- 🐳 **Docker** for containerization
- 🔁 **CI/CD pipelines** for automated deployment
- ☁️ **AWS EC2, S3, and ECR** for scalable cloud infrastructure

This plugin connects to a locally running Flask API (or a cloud-deployed endpoint) to process YouTube video comments, perform sentiment analysis, and visualize keyword patterns—all in real-time within the YouTube interface.

🔧 **Features**

- Sentiment analysis of YouTube comments

- Word cloud and keyword frequency visualizations

- Real-time insights within YouTube

- Uses YouTube Data API v3


#### Frontend View of Plugin running in Chrome (Ex.)


![image](plugin_image_1)

![image](plugin_image_2)

![image](plugin_image_3)


🚀 **Getting Started**

- How to run the backend API (Flask + ML model)

## 🔧 Backend Setup Instructions (Local & EC2)

### 🖥️ Option 1: Run Locally

1. **Create / Activate Environment:**

```bash
conda create --name your-env-name python=3.11		# conda create -n yt-insights-ch-plugin python=3.11

conda activate your-env-name			# conda activate yt-insights-ch-plugin

# OR

python -m venv your-env-name			# python -m venv yt-insights-ch-plugin
source your-env-name/bin/activate		# Linux/Mac OR
your-env-name\Scripts\Activate			# Windows
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Set environment variable for DagsHub access:**

```bash
export DAGSHUB_PAT=<your_dagshub_token>
```

4. **Run the Flask app:**

```bash
python server/app.py
```

5. The app should now be running at:

```
http://localhost:5000
```

6. Swagger documentation is available at:

```
http://localhost:5000/docs
```

---

### ☁️ Option 2: Use Deployed EC2 Backend

> The backend is already deployed to an EC2 instance via CI/CD (GitHub Actions + Docker). You can use it directly by copying the EC2 public URL.

1. Visit the backend live URL in your browser : [http://ec2-13-201-230-148.ap-south-1.compute.amazonaws.com](http://ec2-13-201-230-148.ap-south-1.compute.amazonaws.com)

2. Access Swagger API docs : [http://ec2-13-201-230-148.ap-south-1.compute.amazonaws.com/docs](http://ec2-13-201-230-148.ap-south-1.compute.amazonaws.com/docs)

---

- How to install and use the Chrome extension locally

## 🧩 Chrome Extension Setup (Plugin Integration)

> The plugin fetches sentiment analysis from the backend server and YouTube comment data using the YouTube Data API.

### Step 1: Update `API_URL` and `API_KEY`

Open the plugin file located at:

```
client/popup.js
```

Update the following variables:

```javascript
const API_URL = "http://localhost:5000"; // or your EC2 backend URL
const API_KEY = "<your_youtube_data_api_key>";	// steps to create given in client/README.md
```

- Use `http://localhost:5000` for local testing.
- Use `http://ec2-13-201-230-148.ap-south-1.compute.amazonaws.com` for production (or replace with your deployed public IP).

### Step 2: Load the Plugin

Follow the instructions already provided in the `client/README.md` to:
- Load the unpacked extension in Chrome.
- Test the plugin with updated backend API.

---

🔐 **YouTube API Key Setup**

- Step-by-step guide to get an API key from Google Cloud Console is provided in the `client/README.md`


## 🗃️ Project Organization / Folder Structure (not adhering strictly to following)

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── client             <- Frontend code for Youtube extension
│   ├── README.md       
│   ├── manisfest.json        
│   ├── popup.html      
│   └── popup.js        
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         youtube_insights_chrome_plugin and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
├── server             <- Backend API code
│
|    ├── app.py
|
|    ├── requirements.txt
└── src                <- Source code for use in this project.
|    ├── data                   
|        ├── data_ingestion.py        <- Code to download and generate data
|        │
|        ├── data_preprocessing.py    <- Code to process data
|        │
|    ├── features
|        ├── feature_building.py     <- Code to create features for modeling
|        │
|    ├── model
|        ├── model_building.py            <- Code to train models
|        │
|        ├── model_evaluation.py          <- Code to run model inference with trained models
|        │
|        ├── model_registry.py            <- Code to register model
|        │
   
```

--------


#### DVC PIPELINE

![alt text](dvc_image_final.png)


#### Environment Set (Local)

- conda create -n yt-insights-ch-plugin python=3.11
- conda activate yt-insights-ch-plugin
- pip install -r requirements.txt
- git init
- git remote add 
- git add .
- git commit -m "initial commit"
- git push
- dvc init

#### AWS IAM User

- Create a new user with administrator access in aws and get its access key and secret key and region
- Install AWS cli locally in terminal with boto 3 and run aws configure to set your ACCESS and SECRET ACCESS Key and REGION

#### Setting Up EC2 instance for MLFlow

﻿﻿- sudo apt update: Updates the package list.
﻿﻿- sudo apt install python3-pip: Installs pip for Python 3.
﻿﻿- sudo apt install pipx: Installs pipx for managing Python applications.
- ﻿﻿sudo pipx ensurepath: Ensures pipx path is added to the environment.
﻿﻿- pipx install pipenv: Installs pipenv using pipx.
﻿﻿- export PATH=SPATH:/home/ubuntu/local/bin: Temporarily adds pipenv to the PATH.
﻿﻿- echo 'export PATH=$PATH:/home/ubuntu/local/bin'>>~/.bashre: Permanently adds pipenv to the PATH.
﻿﻿- source ~/.bashre: Applies the changes made to bashre.
﻿﻿- mkdir miflow: Creates a new directory for the project.
- ﻿﻿cd miflow: Navigates into the project directory.
- pipenv shell: Creates and activates a new virtual environment.
- ﻿﻿pipenv install setuptools: Installs setuptools to ensure pkg_resources is available.
﻿﻿- pipenv install miflow: Installs MLflow.
- pipenv install awscli: Installs AWS CLI.
- pipenv install boto3: Installs Botos for AWS SDK..
- aws configure: Configures AWS credentials.(your AWS IAM credentials)
- Aws-key : 
- Aws-secret-key : 
- Aws-region : 
- Mlflow server -h 0.0.0.0 –default-artifiact-root s3://your-s3-storage-name : Starts the MLFlow server on EC2 instance
- Set following in code :
﻿    - ﻿export MLFLOW _TRACKING _URI=http://:5000/: Sets the MLflow tracking URI in the terminal.
﻿﻿    - miflow.set _tracking_uri("http://:5000/"'): Sets the MLflow tracking URI in your code.

#### CodeDeploy Launch Template

```bash
#!/bin/bash

# Update the package list
sudo apt-get update -y

# Install Ruby (required by the CodeDeploy agent)
sudo apt-get install ruby -y

# Download the CodeDeploy agent installer from the correct region
wget https://aws-codedeploy-ap-southeast-2.s3.ap-southeast-2.amazonaws.com/latest/install

# Make the installer executable
chmod +x ./install

# Install the CodeDeploy agent
sudo ./install auto

# Start the CodeDeploy agent
sudo service codedeploy-agent start

sudo service codedeploy-agent status	# on asg instance connect command line
```

#### commands to run on ec2 machine connect terminal (yt-plugin-ec2-ecr-cicd) :

	1. sudo apt-get update
	2. sudo apt-get install -y docker.io
	3. sudo systemctl start docker
	4. sudo systemctl enable docker
	5. sudo apt-get install -y unzip curl
	6. curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
	7. unzip awscliv2.zip
	8. sudo ./aws/install
	9. sudo usermod -aG docker ubuntu
	10. exit
	11. reconnect to terminal to check and type : docker --version

#### Docker run command

```bash
# docker command if deployed through AWS ECR
docker run -p 8888:5000 -e AWS_ACCESS_KEY_ID=YOUR-ACCESS_KEY -e AWS_SECRET_ACCESS_KEY=YOUR-SECRET-ACCESS_KEY niweshbaraj/yt-insights-ch-plugin
```

```bash
# docker command for dagshub
docker run -d -p 80:5000 --name youtube-insights-app -e DAGSHUB_PAT=YOUR-DAGSHUB-API-KEY -e PYTHONPATH=/app niweshbaraj/yt-chrome-plugin-insights:latest
```

#### Add following (as needed) to your github project Repo > Settings > Secrets and variables > Actions > New repository secret

- AWS_ACCESS_KEY_ID				# Through IAM user
- AWS_SECRET_ACCESS_KEY			# Through IAM user
- AWS_DEFAULT_REGION			# Check your AWS region at top right corner
- EC2_HOST						# Create key-pair login to acces your EC2 instance
- EC2_SSH_KEY					# Create key-pair login to acces your EC2 instance
- EC2_USER						# EC2 instance user
- DOCKER_HUB_USERNAME			# Your dockerhub username
- DOCKER_HUB_ACCESS_TOKEN		# Create access token in dockerhub
- DAGSHUB_PAT					# Create token in dagshub

#### `aws configure` - AWS command to run in your local terminal 

- insure aws cli & boto3 is installed in your current environment and type the command `aws configure` in your terminal and press Enter and setup your AWS IAM credentials like following (required to access to AWS resources) :

```bash
AWS Access Key ID [****************JJND]: YOUR-KEY
AWS Secret Access Key [****************mzm4]: YOUR-SECRET-KEY
Default region name [aws-south-1]: YOUR-SELECTED-REGION  # ex : ap-south-1
Default output format [None]:
```

#### (Optional) Manual command to run on EC2 instance connect terminal 

```bash
docker stop youtube-insights-app || true

docker rm youtube-insights-app || true

docker system prune -a -f --volumes

docker pull niweshbaraj/yt-chrome-plugin-insights:latest

docker run -d -p 80:5000 --name youtube-insights-app -e DAGSHUB_PAT=YOUR-ACCESS-TOKEN niweshbaraj/yt-chrome-plugin-insights:latest

docker logs youtube-insights-app		# (optional) to check docker container
```