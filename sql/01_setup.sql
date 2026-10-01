-- Schemas and volumes (run in Databricks SQL Editor)
-- landing:     raw CloudTrail NDJSON files are uploaded here
-- checkpoints: Auto Loader progress bookmarks

CREATE SCHEMA IF NOT EXISTS workspace.sec_raw;
CREATE SCHEMA IF NOT EXISTS workspace.sec_analytics;
CREATE VOLUME IF NOT EXISTS workspace.sec_raw.landing;
CREATE VOLUME IF NOT EXISTS workspace.sec_raw.checkpoints;
