import optuna

def objective(trial):
    alpha = trial.suggest_float("alpha", 0.0, 1.0)

    blended_valid_pred = alpha * lgb_valid_pred + (1 - alpha) * xgb_valid_pred
    auc = roc_auc_score(y_valid, blended_valid_pred)
    return auc

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)

best_alpha = study.best_params["alpha"]
print("Best alpha:", best_alpha)
print("Best blended AUC:", study.best_value)
