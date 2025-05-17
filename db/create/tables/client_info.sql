-- Хранит основную информацию о пользователях Telegram

CREATE TABLE IF NOT EXISTS client_info (
  client_id SERIAL PRIMARY KEY,                                 -- Внутренний ID пользователя в системе
  tg_id INTEGER UNIQUE NOT NULL,                                -- Telegram ID пользователя (внешний идентификатор)
  username TEXT,                                                 -- Telegram username (@...)
  first_name TEXT,                                               -- Имя пользователя
  last_name TEXT,                                                -- Фамилия пользователя
  date_reg DATE,                                                 -- Дата регистрации (впервые начал тренировку)
  email TEXT,                                                    -- Email (если есть, в будущем может использоваться)
  telephone TEXT,                                                -- Телефон (опционально, в будущем для связи)
  language_code TEXT,                                            -- Язык интерфейса Telegram (например, "ru", "en")
  level_id_start INTEGER REFERENCES study_levels(level_id),      -- Уровень, с которого пользователь начал обучение
  level_id_target INTEGER REFERENCES study_levels(level_id)     -- Целевой уровень, к которому стремится
);

-- 📌 Эта таблица:
-- является точкой входа для всех пользователей
-- используется в аналитике, кастомизации, фильтрации
-- содержит ключевые поля для персонализации и определения начального уровня
