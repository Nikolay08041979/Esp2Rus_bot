-- 🧪 Вставка тестовых данных для клиента 1

-- Очистка старых записей
DELETE FROM learned_words WHERE client_id = 1;
DELETE FROM client_activity_words WHERE activity_id IN (
    SELECT id FROM client_activity_log WHERE client_id = 1
);
DELETE FROM client_activity_log WHERE client_id = 1;

-- Уровень A1 (lev_id = 1): 20 слов, все выучены
INSERT INTO learned_words (client_id, word_id, learned_at)
SELECT 1, word_id, CURRENT_DATE
FROM dictionary
WHERE lev_id = 1
LIMIT 20;

-- Уровень A2 (lev_id = 2): 10 слов, выучены
INSERT INTO learned_words (client_id, word_id, learned_at)
SELECT 1, word_id, CURRENT_DATE
FROM dictionary
WHERE lev_id = 2
LIMIT 10;

-- Имитация правильных ответов в client_activity_words
-- (для точности = 100%)
INSERT INTO client_activity_log (client_id, date_login, time_start, time_finish,
    score_quiz, words_correct_quiz, words_incorrect_quiz, level_id_word, quiz_weight)
VALUES
(1, CURRENT_DATE, now(), now(), 1.0, 10, 0, 2, 1.0)
RETURNING id;

-- Подразумеваем, что вернётся ID = 9999 (замените вручную при необходимости)
-- INSERT INTO client_activity_words ...
-- Пример:
-- INSERT INTO client_activity_words (activity_id, word_id, is_correct)
-- VALUES (9999, ..., TRUE), ...;