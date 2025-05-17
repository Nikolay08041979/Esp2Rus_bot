CREATE OR REPLACE VIEW view_study_level_mapped AS
SELECT 
    sl.lev_id, 
    sl.lev_name, 
    s.level_id AS mapped_level_id, 
    s.level_word, 
    s.description
FROM study_level sl
JOIN study_levels s 
    ON LOWER(TRIM(sl.lev_name)) = LOWER(TRIM(s.level_word));

SELECT * FROM view_study_level_mapped;

> SELECT * FROM view_study_level_mapped

lev_id|lev_name   |mapped_level_id|level_word |description                                 |
------+-----------+---------------+-----------+--------------------------------------------+
     1|начальный  |              1|начальный  |Простые фразы, знакомство, базовые выражения|
     1|начальный  |              2|начальный  |Бытовые выражения, семья, покупки           |
     2|средний    |              3|средний    |Повседневные ситуации, путешествия          |
     2|средний    |              4|средний    |Абстрактные темы, беглая речь               |
     3|продвинутый|              5|продвинутый|Свободная речь, сложные тексты              |
     3|продвинутый|              6|продвинутый|Понимание всего, точная речь                |

6 row(s) fetched.