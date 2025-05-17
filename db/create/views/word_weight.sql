-- Отображает вес каждого слова на основе связей:
-- dictionary → study_level → study_levels
-- Используется для точного расчёта quiz_weight по каждому слову

CREATE OR REPLACE VIEW view_word_weight AS
SELECT
  d.word_id,                            -- ID слова из таблицы dictionary
  d.word_src,                           -- Слово на изучаемом языке (универсальное поле, не привязано к конкретному языку)
  d.lev_id,                             -- ID уровня сложности слова (из study_level)
  sl.weight_value                       -- Вес уровня, связанного с этим словом (например, 1.0, 1.3, 1.6)
FROM dictionary d
JOIN study_level sl_map
  ON d.lev_id = sl_map.lev_id           -- Привязка к таблице уровней, используемой в словаре
JOIN study_levels sl
  ON sl_map.lev_name = sl.level_word    -- Связь по названию уровня с официальным справочником
WHERE sl.weight_value IS NOT NULL;      -- Исключаем уровни без веса (чтобы избежать ошибок в расчётах)

-- 📌 Этот VIEW:
-- критически важен для расчёта quiz_weight, если пользователь ответил на все слова
-- обеспечивает точность при агрегации весов слов
-- применяется в calculate_quiz_weight_with_fetch(...)