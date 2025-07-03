import os
import mlflow
import pytest
import pandas as pd
import pickle
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

@pytest.mark.parametrize("model_name, stage", [
    ("yt_chrome_plugin_model", "staging"),
])
def test_model_with_vectorizer(model_name, stage):
    client = MlflowClient()

    # Get the latest version in the specified stage
    latest_version_info = client.get_latest_versions(model_name, stages=[stage])
    latest_version = latest_version_info[0].version if latest_version_info else None

    assert latest_version is not None, f"No model found in the '{stage}' stage for '{model_name}'"

    try:
        # Load the latest version of the model
        model_uri = f"models:/{model_name}/{latest_version}"
        model = mlflow.pyfunc.load_model(model_uri)

        # Create a dummy input for the model
        input_text_df = pd.DataFrame({"clean_comment": ["This is awesome!", "Terrible content"]})

        # Predict using the model
        prediction = model.predict(input_text_df)

        # Verify the output shape
        assert len(prediction) == input_text_df.shape[0], "Output row count mismatch"

        print(f"Model '{model_name}' version {latest_version} successfully processed the dummy input.")

    except Exception as e:
        pytest.fail(f"Model test failed with error: {e}")