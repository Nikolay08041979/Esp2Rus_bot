-- Таблица выученных слов: фиксирует, какие слова пользователь освоил

CREATE TABLE IF NOT EXISTS learned_words (
  client_id INTEGER REFERENCES client_info(client_id),           -- ID пользователя
  word_id INTEGER REFERENCES dictionary(word_id) ON DELETE CASCADE,                -- ID слова, которое считается выученным
  learned_at DATE DEFAULT CURRENT_DATE,                          -- Дата, когда слово было засчитано как выученное
  activity_id INTEGER REFERENCES client_activity_log(id),        -- Сессия викторины, в рамках которой слово было выучено
  PRIMARY KEY (client_id, word_id)                               -- Одно и то же слово может быть выучено только один раз одним пользователем
);


-- 📌 Зачем нужно:
-- основа для фильтрации слов в view_personalized_words
-- используется в аналитике прогресса и автоматического исключения из новых тренировок
-- привязка к activity_id позволяет отследить момент выучивания