DROP TABLE IF EXISTS level_matrix;

CREATE TABLE level_matrix (
    level_id_client INT PRIMARY KEY REFERENCES study_levels(level_id),
    level_client TEXT NOT NULL,
    level_word TEXT NOT NULL,
    lev_id INT NOT NULL REFERENCES table_study_level_mapped(lev_id),
    min_coverage NUMERIC(5,2) NOT NULL,
    min_accuracy NUMERIC(5,2) NOT NULL
);

INSERT INTO level_matrix (
    level_id_client, level_client, level_word, lev_id, min_coverage, min_accuracy
)
SELECT
    level_id,
    level_client,
    level_word,
    lev_id,
    CASE WHEN level_id % 2 = 0 THEN 100.00 ELSE 50.00 END,
    100.00
FROM table_study_level_mapped;
