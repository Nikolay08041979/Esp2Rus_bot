-- 📄 VIEW: client_level_progress
-- Показывает прогресс пользователя по каждому уровню CEFR: coverage и accuracy

DROP VIEW IF EXISTS client_level_progress;

CREATE VIEW client_level_progress AS
WITH total_words_per_level AS (
    SELECT lev_id, COUNT(*) AS total_words
    FROM dictionary
    GROUP BY lev_id
),
learned_words_per_level AS (
    SELECT d.lev_id, lw.client_id, COUNT(*) AS learned_words
    FROM learned_words lw
    JOIN dictionary d ON lw.word_id = d.word_id
    GROUP BY lw.client_id, d.lev_id
)
SELECT
    c.client_id,
    t.lev_id,
    t.total_words,
    COALESCE(l.learned_words, 0) AS learned_words,
    ROUND(COALESCE(l.learned_words, 0) * 100.0 / t.total_words, 1) AS coverage_percent
FROM total_words_per_level t
CROSS JOIN client_info c
LEFT JOIN learned_words_per_level l ON l.client_id = c.client_id AND l.lev_id = t.lev_id;
