DROP TABLE IF EXISTS table_study_level_mapped;

CREATE TABLE table_study_level_mapped (
    lev_id INT NOT NULL UNIQUE,
    lev_name TEXT NOT NULL,
    level_id INT NOT NULL REFERENCES study_levels(level_id),
    level_word TEXT NOT NULL,
    level_client TEXT NOT NULL,
    description TEXT,
    PRIMARY KEY (lev_id, level_id)
);

-- Заполняем таблицу сопоставления, связывая study_level и study_levels по совпадению имени уровня
INSERT INTO table_study_level_mapped (lev_id, lev_name, level_id, level_word, level_client)
SELECT
    sl.lev_id,
    sl.lev_name,
    s.level_id,
    s.level_word,
    s.level_client
FROM study_level sl
JOIN study_levels s
  ON LOWER(TRIM(sl.lev_name)) = LOWER(TRIM(s.level_word))
    ON CONFLICT DO NOTHING;