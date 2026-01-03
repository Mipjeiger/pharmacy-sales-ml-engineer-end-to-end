import joblib
import os
import warnings

warnings.filterwarnings("ignore")
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
MODEL_PATHS = {
    "CatBoostRegressor": os.path.join(
        PROJECT_ROOT, "notebook", "models", "catboost_model.joblib"
    ),
    "LinearRegression": os.path.join(
        PROJECT_ROOT, "notebook", "models", "linear_regression_model.joblib"
    ),
    "RandomForestRegressor": os.path.join(
        PROJECT_ROOT, "notebook", "models", "random_forest_model.joblib"
    ),
}


# see feature importance for each models
def load_models(model_names=str) -> dict:
    models = {}
    for model_name, model in MODEL_PATHS.items():
        if os.path.exists(model):
            models[model_name] = joblib.load(model)
            print(f"{model_name} loaded successfully.")
        else:
            raise FileNotFoundError(f"Model file not found: {model}")
    return models


models = load_models("LinearRegression")

# check feature importance
for model_name, model in models.items():
    print(f"Feature importance for {model_name}:")
    if hasattr(model, "feature_importances_"):
        print(model.feature_importances_)
    else:
        print("Feature importance not available for this model.")

# check coefficients for Linear Regression
if "LinearRegression" in models:
    lr_model = models["LinearRegression"]
    print("Coefficients for Linear Regression:")
    if hasattr(lr_model, "coef_"):
        print(lr_model.coef_)
    else:
        print("Coefficients not available for this model.")
