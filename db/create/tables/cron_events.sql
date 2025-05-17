-- Таблица логов фоновых задач (cron-скриптов, автоматических операций)

CREATE TABLE IF NOT EXISTS cron_events (
  id SERIAL PRIMARY KEY,                                           -- Уникальный ID события
  task_name TEXT NOT NULL,                                         -- Название задачи (например, sync_client_analytics)
  status TEXT NOT NULL,                                            -- Статус выполнения (например: success, failed)
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,                   -- Время запуска задачи (по умолчанию — текущее)
  details TEXT                                                     -- Детали выполнения или сообщение об ошибке
);

-- 📌 Используется для:
-- мониторинга фоновых скриптов (например, расчётов рейтинга, резервного копирования)
-- дебага при сбоях
-- журналирования cron-задач в Telegram или админке