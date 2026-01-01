import mlflow
from mlflow.tracking import MlflowClient

client = MlflowClient()
models = client.search_registered_models()

for model in models:
    print(f"Model Name: {model.name}")
    for v in model.latest_versions:
        print(f" Version: {v.version}, Stage: {v.current_stage}, Run ID: {v.run_id}")
