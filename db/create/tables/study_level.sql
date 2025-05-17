-- Таблица уровней сложности, используемая для маркировки слов в словаре

CREATE TABLE IF NOT EXISTS study_level (
  lev_id SERIAL PRIMARY KEY,                            -- Уникальный ID уровня (например, 1, 2, 3)
  lev_name TEXT NOT NULL                                 -- Название уровня (например, "начальный", "продвинутый")
);

-- Уникальность уровня сложности без учёта регистра
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_level_lower
ON study_level (LOWER(lev_name));                         -- Исключает дубли вроде "Начальный" и "начальный"


--📌 Зачем нужна:
-- используется в dictionary для маркировки уровня сложности слов
-- привязана к study_levels через lev_name (в view_study_level_mapped)
-- основа для генерации персонализированного уровня и веса