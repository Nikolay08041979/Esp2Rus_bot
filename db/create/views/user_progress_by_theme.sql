-- Показывает прогресс пользователя по темам и уровням
CREATE OR REPLACE VIEW view_user_progress_by_theme AS
SELECT
  u.client_id,                 -- ID пользователя
  u.cat_id,                    -- ID темы
  u.level_id,                  -- ID уровня сложности
  wc.cat_name,                 -- Название темы (человеко-читаемое)
  sl.lev_name,                 -- Название уровня (например, "начальный")
  u.total_words,               -- Общее число слов в теме
  u.learned_words,             -- Сколько из них уже выучено
  u.percent_done,              -- Процент выполнения темы (0.00–1.00)
  u.updated_at                 -- Дата последнего обновления
FROM user_progress_by_theme u
JOIN word_category wc ON u.cat_id = wc.cat_id
JOIN study_level sl ON u.level_id = sl.lev_id;


-- 📌 Этот VIEW:
-- используется в админ-панели и пользовательской статистике
-- объединяет user_progress_by_theme с текстами тем и уровней
-- даёт читаемый и готовый к отчётам формат