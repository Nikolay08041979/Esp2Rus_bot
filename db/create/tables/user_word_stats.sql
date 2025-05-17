-- Таблица статистики по каждому слову для каждого пользователя:
-- сколько раз видел, сколько раз ответил правильно и неправильно

CREATE TABLE IF NOT EXISTS user_word_stats (
  client_id INTEGER REFERENCES client_info(client_id),     -- ID пользователя
  word_id INTEGER REFERENCES dictionary(word_id) ON DELETE CASCADE,          -- ID слова
  total_seen INTEGER DEFAULT 0,                            -- Сколько раз слово показывалось в викторинах
  correct INTEGER DEFAULT 0,                               -- Количество правильных ответов по этому слову
  incorrect INTEGER DEFAULT 0,                             -- Количество ошибок по этому слову
  last_seen DATE,                                          -- Дата последнего показа слова пользователю
  PRIMARY KEY (client_id, word_id)                         -- Уникальность: одно слово — один пользователь
);


-- 📌 Эта таблица:
-- используется для формирования learned_words
-- позволяет строить персонализированную динамику и повторение сложных слов
-- может обновляться в момент завершения каждой викторины