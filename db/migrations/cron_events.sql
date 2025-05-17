
-- 📄 cron_events.sql

CREATE TABLE IF NOT EXISTS cron_events (
    id SERIAL PRIMARY KEY,
    task_name TEXT NOT NULL,
    status TEXT NOT NULL,  -- success / failed
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details TEXT
);
