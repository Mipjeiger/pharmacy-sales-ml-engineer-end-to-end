import os
import json
import joblib
import mlflow
import mlflow.sklearn
from dotenv import load_dotenv

# setup

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))  # get current directory path

# load .env file
env_path = os.path.join(PROJECT_ROOT, "..", "..", ".env")
load_dotenv(dotenv_path=env_path)

# registered experiment and model names
EXPERIMENT_NAME = "pharmacy_sales_models"
REGISTERED_MODEL_PREFIX = "pharmacy_sales"

# Load model path
MODELS = {
    "CatBoostRegressor": {
        "model_path": os.path.join(
            PROJECT_ROOT, "../../notebook/models/catboost_model.joblib"
        ),
        "metrics_path": os.path.join(
            PROJECT_ROOT, "../../notebook/metrics/catboost_metrics.json"
        ),
    },
    "LinearRegression": {
        "model_path": os.path.join(
            PROJECT_ROOT, "../../notebook/models/linear_regression_model.joblib"
        ),
        "metrics_path": os.path.join(
            PROJECT_ROOT, "../../notebook/metrics/linear_regression_metrics.json"
        ),
    },
    "RandomForestRegressor": {
        "model_path": os.path.join(
            PROJECT_ROOT, "../../notebook/models/random_forest_model.joblib"
        ),
        "metrics_path": os.path.join(
            PROJECT_ROOT, "../../notebook/metrics/random_forest_metrics.json"
        ),
    },
}

# Optional global metrics path
GLOBAL_METRICS_PATH = os.path.join(
    PROJECT_ROOT, "../../notebook/metrics/all_models_metrics.json"
)


# create a function to load model and metrics
def abs_path(relative_path: str) -> str:
    return os.path.join(PROJECT_ROOT, relative_path)


def load_json(file_path: str) -> dict:
    with open(file_path, "r") as f:
        return json.load(f)


# main function to train and log models
def main():
    print("Starting MLflow model registration")

    mlflow.set_experiment(EXPERIMENT_NAME)

    # Load global metrics for optional use based on global models too
    global_metrics = {}
    global_metrics_file = abs_path(GLOBAL_METRICS_PATH)
    if os.path.exists(global_metrics_file):
        global_metrics = load_json(global_metrics_file)

    # Register each model
    for model_name, cfg in MODELS.items():
        print(f"Registering model: {model_name}")

        model_path = abs_path(cfg["model_path"])
        metrics_path = abs_path(cfg["metrics_path"])

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")

        if not os.path.exists(metrics_path):
            raise FileNotFoundError(f"Metrics file not found: {metrics_path}")

        model = joblib.load(model_path)
        metrics = load_json(metrics_path)

        run_name = f"{model_name}_weekly"

        with mlflow.start_run(run_name=run_name):
            # -- log params --
            mlflow.log_param("model_name", model_name)

            # -- log metrics --
            # Handle nested dicts structure
            for k, v in metrics.items():
                if isinstance(v, dict):
                    # if nested dict, extract the value for this model
                    if model_name in v:
                        mlflow.log_metric(k, float(v[model_name]))
                        print(f"  ✓ Logged metric {k}: {v[model_name]}")
                    else:
                        print(
                            f"  ⚠️  Key '{model_name}' not found in {k}, available keys: {list(v.keys())}"
                        )
                else:
                    # if direct value
                    mlflow.log_metric(k, float(v))
                    print(f"  ✓ Logged metric {k}: {v}")

            # -- log model --
            mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path="model",
                registered_model_name=f"{REGISTERED_MODEL_PREFIX}_{model_name}",
            )

        print(f"✅ {model_name} registration completed.\n")

    print("🎉 All models registered successfully!")


# usage
if __name__ == "__main__":
    main()
