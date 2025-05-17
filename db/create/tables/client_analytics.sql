-- Хранит агрегированную аналитику по каждому пользователю:
-- активность, прогресс, рейтинг и текущий уровень владения языком

CREATE TABLE IF NOT EXISTS client_analytics (
  id SERIAL PRIMARY KEY,                                     -- Уникальный ID записи
  client_id INTEGER UNIQUE REFERENCES client_info(client_id),-- ID пользователя (один к одному)
  last_activity_date DATE,                                   -- Дата последней завершённой викторины
  quizzes_finished_total INTEGER,                            -- Сколько викторин всего пройдено
  quizzes_score_total NUMERIC(3,2),                          -- Суммарный процент успешности (например, 0.83)
  level_id_current INTEGER REFERENCES study_levels(level_id),-- Текущий уровень владения по модели CEFR
  date_level_upgraded DATE,                                  -- Дата последнего повышения уровня
  client_rating NUMERIC(6,2)                                 -- Суммарный рейтинг (на основе quiz_weight)
);

-- 📌 Используется для:
-- отображения /report и /admin_clients
-- расчёта прогресса и адаптации уровня
-- оценки успехов и вовлечённости