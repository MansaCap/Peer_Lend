import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import lightgbm as lgb
import xgboost as xgb
import optuna
import gradio as gr

# -----------------------------
# 1. Load your dataset
# -----------------------------
# Replace with your borrower dataset
# X = pd.read_csv("features.csv")
# y = pd.read_csv("labels.csv")

# Example placeholder
X = pd.DataFrame(np.random.rand(1000, 3), columns=["age","income","group_size"])
y = np.random.randint(0, 2, size=1000)

# -----------------------------
# 2. Train/validation split
# -----------------------------
X_train, X_valid, y_train, y_valid = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# -----------------------------
# 3. LightGBM model
# -----------------------------
lgb_train = lgb.Dataset(X_train, label=y_train)
lgb_valid = lgb.Dataset(X_valid, label=y_valid, reference=lgb_train)

lgb_params = {"objective":"binary","metric":"auc","learning_rate":0.05,"num_leaves":64}
lgb_model = lgb.train(lgb_params, lgb_train, num_boost_round=500,
                      valid_sets=[lgb_valid], early_stopping_rounds=50)

lgb_valid_pred = lgb_model.predict(X_valid, num_iteration=lgb_model.best_iteration)

# -----------------------------
# 4. XGBoost model
# -----------------------------
dtrain = xgb.DMatrix(X_train, label=y_train)
dvalid = xgb.DMatrix(X_valid, label=y_valid)

xgb_params = {"objective":"binary:logistic","eval_metric":"auc","eta":0.05,"max_depth":6}
xgb_model = xgb.train(xgb_params, dtrain, num_boost_round=500,
                      evals=[(dvalid,"valid")], early_stopping_rounds=50)

xgb_valid_pred = xgb_model.predict(dvalid, ntree_limit=xgb_model.best_ntree_limit)

# -----------------------------
# 5. Optuna tuning for alpha
# -----------------------------
def objective(trial):
    alpha = trial.suggest_float("alpha", 0.0, 1.0)
    blended_valid_pred = alpha * lgb_valid_pred + (1 - alpha) * xgb_valid_pred
    return roc_auc_score(y_valid, blended_valid_pred)

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=30)

best_alpha = study.best_params["alpha"]
print("Best alpha:", best_alpha)
print("Best blended AUC:", study.best_value)

# -----------------------------
# 6. Inference function
# -----------------------------
def score_borrower(x_row: pd.DataFrame, alpha=best_alpha) -> float:
    lgb_p = lgb_model.predict(x_row, num_iteration=lgb_model.best_iteration)[0]
    xgb_p = xgb_model.predict(xgb.DMatrix(x_row), ntree_limit=xgb_model.best_ntree_limit)[0]
    return float(alpha * lgb_p + (1 - alpha) * xgb_p)

# -----------------------------
# 7. Gradio admin interface
# -----------------------------
def score_interface(age, income, group_size, alpha):
    x_row = pd.DataFrame([[age, income, group_size]], columns=["age","income","group_size"])
    lgb_p = lgb_model.predict(x_row, num_iteration=lgb_model.best_iteration)[0]
    xgb_p = xgb_model.predict(xgb.DMatrix(x_row), ntree_limit=xgb_model.best_ntree_limit)[0]
    final_p = alpha * lgb_p + (1 - alpha) * xgb_p
    return {
        "LightGBM": round(lgb_p, 4),
        "XGBoost": round(xgb_p, 4),
        "Final Blended": round(final_p, 4)
    }

demo = gr.Interface(
    fn=score_interface,
    inputs=[
        gr.Number(label="Age"),
        gr.Number(label="Monthly Income"),
        gr.Number(label="Group Size"),
        gr.Slider(0, 1, value=best_alpha, step=0.05, label="Alpha (Blend Weight)")
    ],
    outputs="label",
    title="Pulse Lending Risk Engine",
    description="Adjust alpha to balance LightGBM vs XGBoost predictions"
)

if __name__ == "__main__":
    demo.launch()
