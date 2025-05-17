-- VIEW: client_weighted_rating_view
-- Расчёт рейтинга клиента на основе веса викторины

CREATE OR REPLACE VIEW client_weighted_rating_view AS
SELECT
    client_id,
    COUNT(*) AS total_quizzes,
    ROUND(SUM(score_quiz * quiz_weight) / NULLIF(SUM(quiz_weight), 0), 2) AS weighted_score_avg,
    ROUND(SUM(score_quiz * quiz_weight), 2) AS weighted_score_sum,
    ROUND(SUM(quiz_weight), 2) AS total_weight,
    ROUND(SUM(score_quiz * quiz_weight) / NULLIF(SUM(quiz_weight), 0) + LOG(1 + COUNT(*)), 2) AS client_rating
FROM client_activity_log
GROUP BY client_id;