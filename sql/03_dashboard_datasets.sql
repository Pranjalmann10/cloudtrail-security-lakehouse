-- Datasets used by the AI/BI dashboard

-- Dataset: alerts
SELECT * FROM workspace.sec_analytics.alerts;

-- Dataset: alerts_events (raw API calls behind each alert, for drill-down)
SELECT e.identity, e.event_time, e.event_name, e.region, e.source_ip, e.error_code
FROM workspace.sec_analytics.events e
JOIN workspace.sec_analytics.alerts a
  ON e.identity = a.identity
 AND date_trunc('HOUR', e.event_time) = a.hour_bucket;
