# Databricks notebook source
# MAGIC %md
# MAGIC # ingest_nb — Auto Loader ingestion (bronze → silver)
# MAGIC Loads only new files from the `landing` volume. Checkpoints make every run incremental.

# COMMAND ----------

SOURCE = "/Volumes/workspace/sec_raw/landing/"
CKPT = "/Volumes/workspace/sec_raw/checkpoints"

# Bronze: one row per CloudTrail event, stored as raw JSON (VARIANT)
(spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "text")
    .load(SOURCE)
    .selectExpr("parse_json(value) AS v",
                "_metadata.file_path AS file_name",
                "current_timestamp() AS loaded_at")
    .writeStream
    .option("checkpointLocation", f"{CKPT}/bronze")
    .trigger(availableNow=True)
    .toTable("workspace.sec_raw.cloudtrail_raw")
    .awaitTermination())

# COMMAND ----------

# Silver: typed columns extracted from the JSON
(spark.readStream.table("workspace.sec_raw.cloudtrail_raw")
    .selectExpr(
        "try_to_timestamp(v:eventTime::string) AS event_time",
        "v:eventSource::string AS event_source",
        "v:eventName::string AS event_name",
        "v:awsRegion::string AS region",
        "v:sourceIPAddress::string AS source_ip",
        "v:userAgent::string AS user_agent",
        "v:errorCode::string AS error_code",
        "v:userIdentity.type::string AS identity_type",
        "coalesce(v:userIdentity.arn::string, v:userIdentity.principalId::string, "
        "v:userIdentity.type::string) AS identity",
        "v AS raw")
    .writeStream
    .option("checkpointLocation", f"{CKPT}/silver")
    .trigger(availableNow=True)
    .toTable("workspace.sec_analytics.events")
    .awaitTermination())
