import mlflow
from mlflow.tracking import MlflowClient

# Set MLflow tracking URI if hosted on a remote server
mlflow.set_tracking_uri("http://ec2-13-127-25-124.ap-south-1.compute.amazonaws.com:5000/")

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