# Databricks notebook source
# MAGIC %md
# MAGIC # score_nb — score identity-hours and write alerts
# MAGIC Runs automatically after `ingest_nb` in the `ct_pipeline` job.

# COMMAND ----------

import mlflow
import numpy as np

FEATURES = ["n_events", "n_apis", "n_regions", "n_ips", "error_rate",
            "n_sensitive", "n_new_apis", "n_new_ips", "hour_of_day"]

mlflow.set_registry_uri("databricks-uc")
pipe = mlflow.sklearn.load_model("models:/workspace.sec_analytics.ct_iso_forest@champion")

df = spark.table("workspace.sec_analytics.features_hourly").toPandas()
X = df[FEATURES].astype(float)

df["anomaly_score"] = -pipe.decision_function(X)   # higher = more suspicious
df["is_anomaly"] = pipe.predict(X) == -1

z = pipe[:-1].transform(X)                         # scaled features
df["top_feature"] = np.array(FEATURES)[np.abs(z).argmax(axis=1)]

alerts = df[df["is_anomaly"]].sort_values("anomaly_score", ascending=False)
(spark.createDataFrame(alerts)
      .write.mode("overwrite")
      .option("overwriteSchema", "true")
      .saveAsTable("workspace.sec_analytics.alerts"))
