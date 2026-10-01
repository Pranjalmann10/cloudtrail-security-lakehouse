-- Behaviour features: one row per identity per hour.
-- n_new_apis / n_new_ips count first-ever occurrences for that identity.

CREATE OR REPLACE VIEW workspace.sec_analytics.features_hourly AS
WITH firsts AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY identity, event_name ORDER BY event_time) = 1 AS first_api,
    ROW_NUMBER() OVER (PARTITION BY identity, source_ip  ORDER BY event_time) = 1 AS first_ip
  FROM workspace.sec_analytics.events
)
SELECT
  identity,
  date_trunc('HOUR', event_time)           AS hour_bucket,
  COUNT(*)                                 AS n_events,
  COUNT(DISTINCT event_name)               AS n_apis,
  COUNT(DISTINCT region)                   AS n_regions,
  COUNT(DISTINCT source_ip)                AS n_ips,
  AVG(IF(error_code IS NOT NULL, 1, 0))    AS error_rate,
  SUM(IF(event_name IN ('CreateAccessKey','CreateUser','CreateLoginProfile',
                        'AttachUserPolicy','PutUserPolicy','PutBucketPolicy',
                        'UpdateAssumeRolePolicy','GetSecretValue',
                        'StopLogging','DeleteTrail'), 1, 0)) AS n_sensitive,
  SUM(IF(first_api, 1, 0))                 AS n_new_apis,
  SUM(IF(first_ip, 1, 0))                  AS n_new_ips,
  HOUR(date_trunc('HOUR', event_time))     AS hour_of_day
FROM firsts
GROUP BY 1, 2;
