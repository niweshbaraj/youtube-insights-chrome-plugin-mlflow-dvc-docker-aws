import sys
import os
import mlflow
from mlflow.tracking import MlflowClient
from mlflow.exceptions import MlflowException


# Set up DagsHub credentials for MLflow tracking
dagshub_token = os.getenv("DAGSHUB_PAT")

if not dagshub_token:
    raise EnvironmentError("DAGSHUB_PAT environment variable is not set")

os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

dagshub_url = "https://dagshub.com"
repo_owner = "niweshbaraj"
repo_name = "youtube-insights-chrome-plugin-mlflow-dvc-docker-aws"

# Set your remote tracking URI - AWS EC2 MLFlow server
# Make sure to replace with your actual MLFlow server URI
# mlflow.set_tracking_uri("http://ec2-13-127-25-124.ap-south-1.compute.amazonaws.com:5000/")

# Set up MLflow tracking URI
mlflow.set_tracking_uri(f'{dagshub_url}/{repo_owner}/{repo_name}.mlflow')

client = mlflow.MlflowClient()

model_name = "yt_chrome_plugin_model_pipeline"


def promote_model():
    
    # Get the latest version in staging
    staging_versions = client.get_latest_versions(model_name, stages=["Staging"])
    if not staging_versions:
        sys.exit("No model in 'Staging' stage to promote.")

    new_prod_version = staging_versions[0].version
    print(f"✅ Found version v{new_prod_version} in Staging")

    #  Archive existing Production versions (if any)
    prod_versions = client.get_latest_versions(model_name, stages=["Production"])
    if prod_versions:
        for version in prod_versions:
            print(f"📦 Archiving current Production version: v{version.version}")
            client.transition_model_version_stage(
                name=model_name,
                version=version.version,
                stage="Archived"
            )
    else:
        print("No existing Production version")

    # Promote latest Staging to Production
    client.transition_model_version_stage(
        name=model_name,
        version=new_prod_version,
        stage="Production"
    )
    print(f"Model version v{new_prod_version} promoted to Production")

if __name__ == "__main__":
    promote_model()