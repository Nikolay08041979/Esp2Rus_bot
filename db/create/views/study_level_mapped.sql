-- Связка уровней из study_level и study_levels по их именам
-- Используется для сопоставления внутренних и справочных уровней
-- Сравнение происходит без учёта регистра и лишних пробелов
DROP VIEW IF EXISTS view_study_level_mapped CASCADE;

CREATE VIEW view_study_level_mapped AS
SELECT
  sl.lev_id,
  sl.lev_name,
  s.level_id AS mapped_level_id,
  s.level_word,
  s.level_client,
  s.description
FROM study_level sl
JOIN study_levels s
  ON LOWER(TRIM(sl.lev_name)) = LOWER(TRIM(s.level_word));



-- 📌 Этот VIEW:
-- используется во всех связках между словарём и уровнями (через lev_name)
-- применяется в view_quiz_weight_by_group, при расчётах и отображении
-- позволяет гибко сопоставить уровни без жёстких ID