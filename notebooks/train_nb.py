# Databricks notebook source
# MAGIC %md
# MAGIC # train_nb — Isolation Forest + MLflow (Unity Catalog registry)
# MAGIC Run manually when retraining. Registers a new version and points the `champion` alias at it.

# COMMAND ----------

import mlflow
import numpy as np
from mlflow import MlflowClient
from mlflow.models import infer_signature
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler
from sklearn.ensemble import IsolationForest

FEATURES = ["n_events", "n_apis", "n_regions", "n_ips", "error_rate",
            "n_sensitive", "n_new_apis", "n_new_ips", "hour_of_day"]
MODEL_NAME = "workspace.sec_analytics.ct_iso_forest"

X = (spark.table("workspace.sec_analytics.features_hourly")
          .toPandas()[FEATURES].astype(float))

pipe = Pipeline([
    ("log", FunctionTransformer(np.log1p)),
    ("scale", StandardScaler()),
    ("iso", IsolationForest(n_estimators=200, contamination=0.01, random_state=42)),
])
pipe.fit(X)

mlflow.set_registry_uri("databricks-uc")
with mlflow.start_run():
    info = mlflow.sklearn.log_model(
        pipe, "model",
        signature=infer_signature(X, pipe.predict(X)),
        registered_model_name=MODEL_NAME,
    )

MlflowClient().set_registered_model_alias(MODEL_NAME, "champion",
                                          info.registered_model_version)
