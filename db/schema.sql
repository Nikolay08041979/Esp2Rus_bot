-- Создание таблицы категорий
CREATE TABLE IF NOT EXISTS word_category (
  cat_id SERIAL PRIMARY KEY,
  cat_name TEXT NOT NULL  -- Название категории (уникальное, чувствительно к регистру через индекс ниже)
);

-- Уникальность категории без учёта регистра
-- Например: 'Животные' и 'животные' считаются одинаковыми
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_category_lower
ON word_category (LOWER(cat_name));

-- Создание таблицы уровней
CREATE TABLE IF NOT EXISTS study_level (
  lev_id SERIAL PRIMARY KEY,
  lev_name TEXT NOT NULL  -- Название уровня: прилагательное в ед. числе, например 'начальный'
);

-- Уникальность уровня сложности без учёта регистра
-- Например: 'Средний' и 'средний' — дубли
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_level_lower
ON study_level (LOWER(lev_name));

-- Создание таблицы словаря
CREATE TABLE IF NOT EXISTS esp2rus_dictionary (
  word_id SERIAL PRIMARY KEY,
  word_esp TEXT NOT NULL,       -- Слово на испанском
  word_rus TEXT NOT NULL,       -- Корректный перевод
  other_rus1 TEXT NOT NULL,     -- Альтернативный перевод 1
  other_rus2 TEXT NOT NULL,     -- Альтернативный перевод 2
  other_rus3 TEXT NOT NULL,     -- Альтернативный перевод 3
  cat_id INT REFERENCES word_category(cat_id),
  lev_id INT REFERENCES study_level(lev_id)
);

-- Индекс на уникальность слова без учёта регистра
-- Например: 'perro' и 'Perro' считаются одинаковыми
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_word_esp_lower
ON esp2rus_dictionary (LOWER(word_esp));

-- Заполнение категорий (стартовый набор)
-- Значения категорий должны быть в нижнем регистре
INSERT INTO word_category (cat_name) VALUES
  ('животные'),
  ('овощи и фрукты'),
  ('одежда'),
  ('глаголы действия'),
  ('профессии'),
  ('транспорт'),
  ('эмоции'),
  ('природа'),
  ('дом и быт'),
  ('части тела')
ON CONFLICT DO NOTHING;

-- Заполнение уровней сложности (прилагательные в ед. числе, без повторов)
-- Значения уровней должны быть в нижнем регистре
INSERT INTO study_level (lev_name) VALUES
  ('начальный'),
  ('средний'),
  ('продвинутый')
ON CONFLICT DO NOTHING;

-- Удаление всех записей из словаря
TRUNCATE TABLE esp2rus_dictionary RESTART IDENTITY CASCADE;

-- Очистка таблицы категорий
TRUNCATE TABLE word_category RESTART IDENTITY CASCADE;

-- Очистка таблицы уровней
TRUNCATE TABLE study_level RESTART IDENTITY CASCADE;
