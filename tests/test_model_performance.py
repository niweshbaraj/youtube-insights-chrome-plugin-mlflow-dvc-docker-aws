import os
import pytest
import pandas as pd
import pickle
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import mlflow

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

@pytest.mark.parametrize("model_name, stage, holdout_data_path", [
    ("yt_chrome_plugin_model_pipeline", "staging", "data/interim/test_processed.csv"),  # Replace with your actual paths
])
def test_model_performance(model_name, stage, holdout_data_path):
    try:
        # Load the model from MLflow
        client = mlflow.tracking.MlflowClient()
        latest_version_info = client.get_latest_versions(model_name, stages=[stage])
        latest_version = latest_version_info[0].version if latest_version_info else None

        assert latest_version is not None, f"No model found in the '{stage}' stage for '{model_name}'"

        model_uri = f"models:/{model_name}/{latest_version}"
        model = mlflow.pyfunc.load_model(model_uri)

        # Load the holdout test data
        holdout = pd.read_csv(holdout_data_path)
        X_holdout = holdout["clean_comment"].fillna("")
        y_holdout = holdout["category"]

        # Predict using the model
        y_pred_new = model.predict(pd.DataFrame({"clean_comment": X_holdout}))

        # Calculate performance metrics
        accuracy_new = accuracy_score(y_holdout, y_pred_new)
        precision_new = precision_score(y_holdout, y_pred_new, average='weighted', zero_division=1)
        recall_new = recall_score(y_holdout, y_pred_new, average='weighted', zero_division=1)
        f1_new = f1_score(y_holdout, y_pred_new, average='weighted', zero_division=1)


        # Define expected thresholds for the performance metrics
        expected_accuracy = 0.40
        expected_precision = 0.40
        expected_recall = 0.40
        expected_f1 = 0.40

        # Assert that the new model meets the performance thresholds
        assert accuracy_new >= expected_accuracy, f'Accuracy should be at least {expected_accuracy}, got {accuracy_new}'
        assert precision_new >= expected_precision, f'Precision should be at least {expected_precision}, got {precision_new}'
        assert recall_new >= expected_recall, f'Recall should be at least {expected_recall}, got {recall_new}'
        assert f1_new >= expected_f1, f'F1 score should be at least {expected_f1}, got {f1_new}'

        print(f"Performance test passed for model '{model_name}' version {latest_version}")

    except Exception as e:
        pytest.fail(f"Model performance test failed with error: {e}")