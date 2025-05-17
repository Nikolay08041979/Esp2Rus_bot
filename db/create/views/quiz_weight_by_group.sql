-- Возвращает максимальный вес уровня для каждого lev_id через view_study_level_mapped
-- Используется для расчёта quiz_weight, если известен только lev_id (без слов)

CREATE OR REPLACE VIEW view_quiz_weight_by_group AS
SELECT
  vslm.lev_id,                           -- ID уровня из study_level (например, 1 — начальный)
  MAX(sl.weight_value) AS weight_value  -- Максимальный вес, присвоенный этому уровню (например, 1.3)
FROM view_study_level_mapped vslm
JOIN study_levels sl
  ON sl.level_word = vslm.level_word     -- Связь по названию уровня, приводим к общему виду
GROUP BY vslm.lev_id                     -- Группируем по уровню из study_level
ORDER BY vslm.lev_id;                    -- Для читаемости и предсказуемости результата

-- 📌 Применяется в логике:
-- когда score_quiz < 1.0 и нет смысла рассчитывать вес по словам
-- в обобщённой аналитике без детализации слов