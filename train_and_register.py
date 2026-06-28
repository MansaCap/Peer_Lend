import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from mlflow.tracking import MlflowClient

# Load data
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y)

# Train model
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Log model
with mlflow.start_run() as run:
    mlflow.sklearn.log_model(clf, "model")

    run_id = run.info.run_id

# Register model
result = mlflow.register_model(
    f"runs:/{run_id}/model", "RiskModel"
)

# Promote to Production
client = MlflowClient()
client.transition_model_version_stage(
    name="RiskModel",
    version=1,
    stage="Production"
)

print("Model registered and promoted to Production.")
