from fastapi import FastAPI
import pandas as pd 
import lightgbm as lgb
import xgboost as xgb
from Risk_EngineCore import score_borrower  # import your scoring function

app = FastAPI(title="Pulse Lending Risk Engine API")

@app.post("/score")
def score_endpoint(age: float, income: float, group_size: int, alpha: float = 0.5):
    """
    Score a borrower using blended LightGBM + XGBoost.
    """
    x_row = pd.DataFrame([[age, income, group_size]], columns=["age","income","group_size"])
    risk_score = score_borrower(x_row, alpha=alpha)
    return {"risk_score": risk_score}
