-- Основной словарь: слова на изучаемом языке + перевод и уровень сложности

CREATE TABLE IF NOT EXISTS dictionary (
  word_id SERIAL PRIMARY KEY,                                    -- Уникальный ID слова
  word_src TEXT NOT NULL,                                        -- Слово на изучаемом языке (универсальное поле: может быть испанское, немецкое и т.д.)
  word_rus TEXT NOT NULL,                                        -- Перевод на русский язык
  other_rus1 TEXT NOT NULL,                                      -- Альтернативный перевод 1
  other_rus2 TEXT NOT NULL,                                      -- Альтернативный перевод 2
  other_rus3 TEXT NOT NULL,                                      -- Альтернативный перевод 3
  cat_id INT REFERENCES word_category(cat_id),                   -- ID категории (тема слова)
  lev_id INT REFERENCES study_level(lev_id)                      -- ID уровня сложности (например, "начальный")
);

-- Индекс на уникальность исходного слова без учёта регистра
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_word_src_lower
ON dictionary (LOWER(word_src));

-- 📌 Особенности:
-- Структура готова к масштабированию на другие языки
-- Индекс LOWER(word_src) предотвращает дубликаты в словаре, даже если Hola и hola
-- cat_id и lev_id дают гибкую привязку к теме и уровню