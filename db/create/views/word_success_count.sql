-- 🔍 VIEW: word_success_count
-- 📌 Назначение:
-- Для каждого пользователя и каждого слова считает:
--   - общее число попыток (total_attempts)
--   - количество правильных ответов (correct_count)
-- Используется для определения, выучено ли слово (если correct_count >= 3).

-- 💡 Это ядро логики персонализации: если слово было правильно переведено 3 и более раз,
-- оно может считаться "выученным" и быть исключено из следующих викторин.

CREATE OR REPLACE VIEW word_success_count AS
SELECT
    cal.client_id,         -- идентификатор пользователя
    caw.word_id,           -- идентификатор слова
    COUNT(*) FILTER (WHERE caw.is_correct = TRUE) AS correct_count,  -- число успешных попыток
    COUNT(*) AS total_attempts                                      -- общее число попыток
FROM client_activity_words caw
JOIN client_activity_log cal ON cal.id = caw.activity_id
GROUP BY cal.client_id, caw.word_id;
