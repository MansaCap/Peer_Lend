import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import lightgbm as lgb
import xgboost as xgb

# Train/validation split
X_train, X_valid, y_train, y_valid = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# --- LightGBM ---
lgb_train = lgb.Dataset(X_train, label=y_train)
lgb_valid = lgb.Dataset(X_valid, label=y_valid, reference=lgb_train)

lgb_params = {"objective":"binary","metric":"auc","learning_rate":0.05,"num_leaves":64}
lgb_model = lgb.train(lgb_params, lgb_train, num_boost_round=500,
                      valid_sets=[lgb_valid], early_stopping_rounds=50)

lgb_valid_pred = lgb_model.predict(X_valid, num_iteration=lgb_model.best_iteration)

# --- XGBoost ---
dtrain = xgb.DMatrix(X_train, label=y_train)
dvalid = xgb.DMatrix(X_valid, label=y_valid)

xgb_params = {"objective":"binary:logistic","eval_metric":"auc","eta":0.05,"max_depth":6}
xgb_model = xgb.train(xgb_params, dtrain, num_boost_round=500,
                      evals=[(dvalid,"valid")], early_stopping_rounds=50)

xgb_valid_pred = xgb_model.predict(dvalid, ntree_limit=xgb_model.best_ntree_limit)

# --- Blending ---
alpha = 0.6  # weight for LightGBM (tune this)
blended_valid_pred = alpha * lgb_valid_pred + (1 - alpha) * xgb_valid_pred

print("LightGBM AUC:", roc_auc_score(y_valid, lgb_valid_pred))
print("XGBoost AUC:", roc_auc_score(y_valid, xgb_valid_pred))
print("Blended AUC:", roc_auc_score(y_valid, blended_valid_pred))

# --- Inference function ---
def score_borrower(x_row: pd.DataFrame, alpha=0.6) -> float:
    lgb_p = lgb_model.predict(x_row, num_iteration=lgb_model.best_iteration)[0]
    xgb_p = xgb_model.predict(xgb.DMatrix(x_row), ntree_limit=xgb_model.best_ntree_limit)[0]
    return float(alpha * lgb_p + (1 - alpha) * xgb_p)
