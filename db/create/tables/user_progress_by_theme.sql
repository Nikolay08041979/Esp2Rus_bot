-- Таблица, отражающая прогресс пользователя по каждой теме и уровню

-- 🔧 Создание таблицы user_progress_by_theme (если не создана ранее)
CREATE TABLE IF NOT EXISTS user_progress_by_theme (
  client_id INTEGER REFERENCES client_info(client_id),        -- ID пользователя
  cat_id INTEGER REFERENCES word_category(cat_id),            -- ID категории слов (темы)
  level_id INTEGER REFERENCES study_level(lev_id),            -- ID уровня сложности
  total_words INTEGER,                                        -- Общее количество слов в теме и уровне
  learned_words INTEGER,                                      -- Количество выученных слов из total_words
  percent_done NUMERIC(5,2),                                  -- Процент выполнения темы: 0.00–100.00
  updated_at DATE DEFAULT CURRENT_DATE,                       -- Дата последнего обновления прогресса
  PRIMARY KEY (client_id, cat_id, level_id)                   -- Каждая тема и уровень уникальны для пользователя
);


-- 📌 Эта таблица:
-- нужна для отображения прогресса в отчетах и UI
-- используется для расчёта общей завершенности и определения готовности к следующему уровню
-- может обновляться cron-скриптом или после викторины