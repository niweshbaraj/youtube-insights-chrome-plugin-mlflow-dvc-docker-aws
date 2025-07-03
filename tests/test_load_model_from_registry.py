import os
import mlflow
from mlflow.tracking import MlflowClient

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

# Set up MLflow tracking URI
mlflow.set_tracking_uri(f'{dagshub_url}/{repo_owner}/{repo_name}.mlflow')

# Load model from the model registry
# def load_model_from_registry(model_name: str, stage: str = "Staging"):
#     """Load a model from the MLflow Model Registry."""
#     try:
#         client = MlflowClient()
#         model_version = client.get_latest_versions(model_name, stages=[stage])[0]
#         model_uri = f"models:/{model_name}/{model_version.version}"
#         model = mlflow.pyfunc.load_model(model_uri)
#         return model
#     except Exception as e:
#         print(f"Error loading model {model_name} from stage {stage}: {e}")
#         raise

def load_model_from_registry(model_name: str, model_version: str):
    """Load a model from the MLflow Model Registry."""
    try:
        model_uri = f"models:/{model_name}/{model_version}"
        model = mlflow.pyfunc.load_model(model_uri)
        return model
    except Exception as e:
        print(f"Error loading model {model_name} from version {model_version}: {e}")
        raise

# Example usage
model_name = "yt_chrome_plugin_model"  # Replace with your model name
model_version = "1"  # Replace with your model version
model = load_model_from_registry(model_name, model_version)
print(f"Model '{model_name}' loaded successfully.")