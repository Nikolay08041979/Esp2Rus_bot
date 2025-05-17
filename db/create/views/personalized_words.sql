-- 📄 VIEW: view_personalized_words
-- Показывает список всех слов, ещё не выученных каждым пользователем
-- Перестраивается каждый раз динамически (персонализированная выдача)

DROP VIEW IF EXISTS view_personalized_words;

CREATE VIEW view_personalized_words AS
SELECT
  d.word_id,
  d.word_src,
  d.word_rus,
  d.other_rus1,
  d.other_rus2,
  d.other_rus3,
  d.cat_id,
  wc.cat_name AS category,
  d.lev_id,
  sl.lev_name AS level,
  c.client_id
FROM dictionary d
JOIN word_category wc ON d.cat_id = wc.cat_id
JOIN study_level sl ON d.lev_id = sl.lev_id
CROSS JOIN client_info c
WHERE NOT EXISTS (
  SELECT 1 FROM learned_words lw
  WHERE lw.client_id = c.client_id AND lw.word_id = d.word_id
);