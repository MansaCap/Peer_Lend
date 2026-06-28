import numpy as np
import pandas as pd
import streamlit as st
import lightgbm as lgb
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import shap

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
# 4. Streamlit Admin UI
# -----------------------------
st.title("Pulse Lending Risk Engine v2")
st.sidebar.header("Admin Controls")

alpha = st.sidebar.slider("Blend Weight (Alpha)", 0.0, 1.0, 0.5, 0.05)

# Blended predictions
blended_valid_pred = alpha * lgb_valid_pred + (1 - alpha) * xgb_valid_pred
auc_score = roc_auc_score(y_valid, blended_valid_pred)

st.write(f"### Current Validation AUC: {auc_score:.4f}")
st.write(f"LightGBM AUC: {roc_auc_score(y_valid, lgb_valid_pred):.4f}")
st.write(f"XGBoost AUC: {roc_auc_score(y_valid, xgb_valid_pred):.4f}")

# -----------------------------
# 5. Borrower Scoring Form
# -----------------------------
st.header("Borrower Risk Scoring")
age = st.number_input("Age", min_value=18, max_value=80, value=30)
income = st.number_input("Monthly Income", min_value=0, max_value=10000, value=500)
group_size = st.number_input("Group Size", min_value=1, max_value=20, value=5)

x_row = pd.DataFrame([[age, income, group_size]], columns=["age","income","group_size"])
lgb_p = lgb_model.predict(x_row, num_iteration=lgb_model.best_iteration)[0]
xgb_p = xgb_model.predict(xgb.DMatrix(x_row), ntree_limit=xgb_model.best_ntree_limit)[0]
final_p = alpha * lgb_p + (1 - alpha) * xgb_p

st.write("### Borrower Risk Scores")
st.write(f"LightGBM: {lgb_p:.4f}")
st.write(f"XGBoost: {xgb_p:.4f}")
st.write(f"Final Blended: {final_p:.4f}")

# -----------------------------
# 6. SHAP Explainability
# -----------------------------
st.header("Explainability (SHAP)")
explainer = shap.TreeExplainer(lgb_model)
shap_values = explainer.shap_values(X_valid[:100])  # sample for speed

st.write("Feature importance (LightGBM):")
shap.summary_plot(shap_values, X_valid[:100], plot_type="bar", show=False)
st.pyplot(bbox_inches="tight")
