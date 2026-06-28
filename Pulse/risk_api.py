from fastapi import FastAPI
import pandas as pd
import mlflow

app = FastAPI(title="Pulse Lending Risk Engine API")

# Load registered models from MLflow
lgb_model = mlflow.sklearn.load_model("models:/Pulse_Lending_LightGBM/Production")
xgb_model = mlflow.sklearn.load_model("models:/Pulse_Lending_XGBoost/Production")

@app.post("/score")
def score_endpoint(age: float, income: float, group_size: int, alpha: float = 0.5):
    x_row = pd.DataFrame([[age, income, group_size]], columns=["age","income","group_size"])
    lgb_p = lgb_model.predict(x_row)[0]
    xgb_p = xgb_model.predict(x_row)[0]
    final_p = alpha * lgb_p + (1 - alpha) * xgb_p
    return {"risk_score": final_p}
