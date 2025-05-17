CREATE OR REPLACE VIEW view_quiz_weight_by_group AS
SELECT
    sl.level_id AS lev_id,           -- 1–6 (из словаря)
    vslm.level_group_id AS group_id, -- 1–3 (начальный, средний, продвинутый)
    sl.weight_value
FROM study_levels sl
JOIN view_study_level_mapped vslm ON sl.level_id = vslm.level_id_word;
