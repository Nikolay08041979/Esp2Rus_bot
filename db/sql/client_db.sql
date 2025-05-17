
-- Таблица 1: Статичные данные клиента
CREATE TABLE IF NOT EXISTS client_info (
    client_id SERIAL PRIMARY KEY,
    client_tg_id INTEGER NOT NULL,
    client_username TEXT,
    client_fname TEXT,
    client_lname TEXT,
    client_date_reg DATE,
    client_email TEXT,
    client_telephone TEXT,
    client_language_code TEXT,
    level_id_start INTEGER REFERENCES study_levels(level_id_client),
    level_id_target INTEGER REFERENCES study_levels(level_id_client)
);

-- Таблица 2: История активности по викторинам
CREATE TABLE IF NOT EXISTS client_activity_log (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES client_info(client_id),
    date_login DATE,
    time_start TIME,
    time_finish TIME,
    score_quiz NUMERIC(3,2),
    words_correct_quiz INTEGER,
    words_incorrect_quiz INTEGER
);

-- Таблица 3: Агрегированная аналитика
CREATE TABLE IF NOT EXISTS client_analytics (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES client_info(client_id),
    client_last_activity_date DATE,
    quizes_finished_total INTEGER,
    quizes_score_total NUMERIC(3,2),
    level_id_current INTEGER REFERENCES study_levels(level_id_client),
    raiting_client NUMERIC(3,2)
);

-- Таблица 4: CEFR уровни + уровни слов
CREATE TABLE IF NOT EXISTS study_levels (
    level_id_client INTEGER PRIMARY KEY,
    level_client TEXT,
    level_id_word INTEGER,
    level_word TEXT,
    description TEXT
);

-- Наполнение справочника уровней испанского языка
INSERT INTO study_levels (level_id_client, level_client, level_id_word, level_word, description) VALUES
(1, 'a1 — начальный (beginner)', 1, 'начинающий', 'Простые фразы, знакомство, базовые выражения'),
(2, 'a2 — элементарный (elementary)', 1, 'начинающий', 'Бытовые выражения, семья, покупки'),
(3, 'b1 — средний (intermediate)', 2, 'средний', 'Повседневные ситуации, путешествия'),
(4, 'b2 — выше среднего (upper-intermediate)', 2, 'средний', 'Абстрактные темы, беглая речь'),
(5, 'c1 — продвинутый (advanced)', 3, 'продвинутый', 'Свободная речь, сложные тексты'),
(6, 'c2 — владение в совершенстве (proficient)', 3, 'продвинутый', 'Понимание всего, точная речь')
ON CONFLICT (level_id_client) DO NOTHING;
