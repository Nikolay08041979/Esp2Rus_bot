-- Хранит информацию о прохождении викторины пользователем

-- Хранит список слов, участвовавших в каждой викторине, и правильность ответа

CREATE TABLE IF NOT EXISTS client_activity_words (
  activity_id INT NOT NULL REFERENCES client_activity_log(id) ON DELETE CASCADE,  -- ID сессии викторины
  word_id INT NOT NULL REFERENCES dictionary(word_id) ON DELETE CASCADE,           -- ID слова
  is_correct BOOLEAN NOT NULL,                                                      -- Был ли ответ правильным (true/false)
  PRIMARY KEY (activity_id, word_id)                                                -- Одно слово один раз в сессии
);


-- 📌 Эта таблица:
-- используется для расчёта learned_words, user_word_stats
-- позволяет отслеживать успехи по каждому слову
-- связана с client_activity_log и dictionary через ON DELETE CASCADE