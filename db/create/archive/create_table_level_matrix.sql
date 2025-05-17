CREATE OR REPLACE VIEW level_matrix AS
SELECT
  ROW_NUMBER() OVER (ORDER BY vslm.mapped_level_id) AS level_id_client,  -- ID для клиента
  vslm.level_client AS cefr_id,                                           -- A1, A2, ..., C2
  vslm.lev_name AS level_name,                                            -- начальный, средний, продвинутый
  vslm.lev_id,                                                            -- ID уровня из study_level
  CASE
    WHEN vslm.mapped_level_id % 2 = 1 THEN 50.00
    ELSE 100.00
  END AS min_coverage,                                                    -- 50% для первой ступени, 100% для второй
  100.00 AS min_accuracy                                                  -- Всегда 100%
FROM view_study_level_mapped vslm
ORDER BY vslm.mapped_level_id;
