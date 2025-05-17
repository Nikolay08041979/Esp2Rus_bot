-- Подсчёт количества слов в каждой категории (по всем уровням)
SELECT
    c.cat_name AS категория,
    COUNT(d.word_id) AS количество_слов
FROM
    dictionary d
JOIN
    word_category c ON d.cat_id = c.cat_id
GROUP BY
    c.cat_name
ORDER BY
    количество_слов DESC;



-- Подсчёт количества слов по категориям и уровням сложности
SELECT
    c.cat_name AS категория,
    l.lev_name AS уровень,
    COUNT(d.word_id) AS количество_слов
FROM
    dictionary d
JOIN
    word_category c ON d.cat_id = c.cat_id
JOIN
    study_level l ON d.lev_id = l.lev_id
GROUP BY
    c.cat_name, l.lev_name
ORDER BY
    c.cat_name, l.lev_name;

