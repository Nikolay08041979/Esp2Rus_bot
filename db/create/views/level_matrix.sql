CREATE OR REPLACE VIEW level_matrix AS
SELECT
  ROW_NUMBER() OVER (ORDER BY vslm.mapped_level_id) AS level_id_client,
  vslm.level_client AS cefr_id,
  UPPER(SPLIT_PART(vslm.level_client, ' ', 1)) AS cefr_id_short,
  vslm.lev_name AS level_name,
  vslm.lev_id,
  CASE
    WHEN vslm.mapped_level_id % 2 = 1 THEN 50.00
    ELSE 100.00
  END AS min_coverage
FROM view_study_level_mapped vslm
ORDER BY vslm.mapped_level_id;
