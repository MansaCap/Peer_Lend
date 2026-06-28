import numpy as np
import pandas as pd
import lightgbm as lgb
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

# -----------------------------
# 1. Load dataset (replace with real borrower data)
# -----------------------------
X = pd.DataFrame(np.random.rand(1000, 3), columns=["age","income","group_size"])
y = np.random.randint(0, 2, size=1000)

X_train, X_valid, y_train, y_valid = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# -----------------------------
# 2. Train LightGBM
# -----------------------------
lgb_train = lgb.Dataset(X_train, label=y_train)
lgb_valid = lgb.Dataset(X_valid, label=y_valid, reference=lgb_train)

lgb_params = {"objective":"binary","metric":"auc","learning_rate":0.05,"num_leaves":64}
lgb_model = lgb.train(lgb_params, lgb_train, num_boost_round=300,
                      valid_sets=[lgb_valid], early_stopping_rounds=50)

lgb_valid_pred = lgb_model.predict(X_valid, num_iteration=lgb_model.best_iteration)

# -----------------------------
# 3. Train XGBoost
# -----------------------------
dtrain = xgb.DMatrix(X_train, label=y_train)
dvalid = xgb.DMatrix(X_valid, label=y_valid)

xgb_params = {"objective":"binary:logistic","eval_metric":"auc","eta":0.05,"max_depth":6}
xgb_model = xgb.train(xgb_params, dtrain, num_boost_round=300,
                      evals=[(dvalid,"valid")], early_stopping_rounds=50)

xgb_valid_pred = xgb_model.predict(dvalid, ntree_limit=xgb_model.best_ntree_limit)

# -----------------------------
# 4. Blending (fixed alpha)
# -----------------------------
alpha = 0.5  # adjust or tune externally
blended_valid_pred = alpha * lgb_valid_pred + (1 - alpha) * xgb_valid_pred

print("LightGBM AUC:", roc_auc_score(y_valid, lgb_valid_pred))
print("XGBoost AUC:", roc_auc_score(y_valid, xgb_valid_pred))
print("Blended AUC:", roc_auc_score(y_valid, blended_valid_pred))

# -----------------------------
# 5. Scoring function
# -----------------------------
def score_borrower(x_row: pd.DataFrame, alpha=alpha) -> float:
    """
    x_row: single-row DataFrame with same columns as training X
    returns: final blended default probability (0–1)
    """
    lgb_p = lgb_model.predict(x_row, num_iteration=lgb_model.best_iteration)[0]
    xgb_p = xgb_model.predict(xgb.DMatrix(x_row), ntree_limit=xgb_model.best_ntree_limit)[0]
    return float(alpha * lgb_p + (1 - alpha) * xgb_p)
