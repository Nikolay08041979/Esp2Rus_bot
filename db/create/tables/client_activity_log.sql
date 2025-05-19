-- Хранит информацию о прохождении викторины пользователем

CREATE TABLE IF NOT EXISTS client_activity_log (
  id SERIAL PRIMARY KEY,                                   -- Уникальный ID сессии викторины
  client_id INTEGER REFERENCES client_info(client_id),     -- ID пользователя, прошедшего викторину
  date_login DATE,                                         -- Дата запуска сессии
  time_start TIME,                                         -- Время начала викторины
  time_finish TIME,                                        -- Время окончания викторины
  score_quiz NUMERIC(3,2),                                 -- Общий результат (доля правильных ответов, например 0.85)
  words_correct_quiz INTEGER,                              -- Количество правильно отвеченных слов
  words_incorrect_quiz INTEGER,                            -- Количество ошибок
  level_id_word INTEGER REFERENCES study_levels(level_id), -- Уровень слов, использованных в этой викторине (1-3 или NULL если "все уровни")
  quiz_weight NUMERIC(3,2)                                 -- Расчётный вес сложности викторины
);

-- 📌 Это таблица №1 для:
-- логирования каждой сессии
-- анализа успешности
-- расчёта рейтинга, уровня, сложности