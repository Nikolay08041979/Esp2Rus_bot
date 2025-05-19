-- 🔄 Обновление VIEW: view_user_progress_by_theme
-- Показывает прогресс пользователя по темам (без учёта уровня)
CREATE VIEW view_user_progress_by_theme AS
SELECT
    c.client_id,
    cat.cat_id,
    cat.cat_name,
    COUNT(*) FILTER (WHERE d.word_id IS NOT NULL) AS total_words,
    COUNT(lw.word_id) AS learned_words,
    ROUND(
        COUNT(lw.word_id) * 100.0 / NULLIF(COUNT(*) FILTER (WHERE d.word_id IS NOT NULL), 0),
        2
    ) AS percent_done,
    CURRENT_DATE AS updated_at
FROM dictionary d
JOIN word_category cat ON d.cat_id = cat.cat_id
CROSS JOIN (SELECT DISTINCT client_id FROM learned_words) c
LEFT JOIN learned_words lw ON lw.word_id = d.word_id AND lw.client_id = c.client_id
GROUP BY c.client_id, cat.cat_id, cat.cat_name;



-- используется в админ-панели и пользовательской статистике
-- объединяет user_progress_by_theme с текстами тем и уровней
-- даёт читаемый и готовый к отчётам формат