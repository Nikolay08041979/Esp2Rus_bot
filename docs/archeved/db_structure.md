# 📦 Структура базы данных

### Таблица #1: dictionary
- word_id (PK, serial)
- word_src (text)
- word_rus (text)
- other_rus1, other_rus2, other_rus3 (text)
- cat_id (FK → word_category)
- lev_id (FK → study_level)

### Таблица #2: word_category
- cat_id (PK)
- cat_name (text)

### Таблица #3: study_Level
- lev_id (PK)
- lev_name (text) — «начальный», «средний», «продвинутый»

#### 📦 Структура базы данных (SQL)

##### ![Архитектура БД проекта (этап MVP)](db/schema_v1.png)

##### [📄 SQL-скрипт для создания таблиц БД](db/schema.sql)


### Таблица #4: client_db (на перспективу)
- id (PK)
- client_id (integer)
- client_tgnick (text)
- date_reg (date)
- date_last_login (date)
- correct_words (array of word_id)
- client_rating (integer) — общее число правильных ответов (необходимо уточнить расчёт, включив в него LTV)

