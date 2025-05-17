-- Создание таблицы категорий слов (тем), например: "Путешествия", "Еда", "Работа"

CREATE TABLE IF NOT EXISTS word_category (
  cat_id SERIAL PRIMARY KEY,                                -- Уникальный ID категории
  cat_name TEXT NOT NULL                                     -- Название категории (например, "Путешествия")
);

-- Уникальность категории без учёта регистра
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_category_lower
ON word_category (LOWER(cat_name));                          -- Запрещает дубли: "еда" и "Еда"



-- 📌 Эта таблица:
-- используется в dictionary через cat_id
-- отображается в UI для выбора темы
-- обеспечивает единую структуру тем без дубликатов