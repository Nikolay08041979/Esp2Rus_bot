# 🧠 Esp2Rus_bot — Техническое задание: Персонализация обучения (v2)

## 🎯 Цель
Построить персональный маршрут обучения для каждого пользователя, в котором:
- Слова считаются выученными при многократном подтверждённом знании
- Прогресс по темам и уровням отслеживается и обновляется автоматически
- Уровень владения определяется по охвату и точности
- Повторения регулируются на основе истории активности

## 📁 Структура персонализации

```
analytics/
├── save_client_activity_log.py       # записывает stats, learned_words
├── save_client_analytics.py          # обновляет рейтинг, прогресс, уровень
├── calculate_client_id_current.py    # логика присвоения уровня по матрице
├── metrics/
│   ├── get_level_id_word.py
│   ├── calculate_quiz_weight.py
│   └── ...
db/
├── create/
│   ├── learned_words.sql
│   ├── user_word_stats.sql
│   ├── user_progress_by_theme.sql
│   ├── level_matrix.sql
│   └── ...
```

---

## 📦 База данных: таблицы

### 1. learned_words

Хранит факт выучивания слова на основе количества успешных повторений.

| Поле         | Тип     | Описание                              |
|--------------|---------|---------------------------------------|
| client_id    | int     | ID пользователя (из `client_info`)    |
| word_id      | int     | ID слова (из `dictionary`)                     |
| learned_at   | date    | Дата выучивания                       |
| activity_id  | int     | Ссылка на викторину (client_activity) |

🔁 Слово считается выученным после `N` правильных ответов  
`N` задаётся в `LEARN_THRESHOLD = 3` (в `settings.py` или `config.py`)

---

### 2. user_word_stats

Хранит детальную статистику по каждому слову.

| Поле         | Тип     | Описание                           |
|--------------|---------|------------------------------------|
| client_id    | int     | ID пользователя (из `client_info`) |
| word_id      | int     | ID слова (из `dictionary`)                          |
| total_seen   | int     | Сколько раз слово показывалось     |
| correct      | int     | Кол-во правильных ответов          |
| incorrect    | int     | Кол-во ошибок                      |
| last_seen    | date    | Последняя попытка                  |

---

### 3. user_progress_by_theme

Отображает прогресс пользователя по теме на текущем уровне.

| Поле         | Тип     | Описание                              |
|--------------|---------|----------------------------------------|
| client_id    | int     | ID пользователя (из `client_info`)                       |
| cat_id       | int     | ID темы (из `word_category`)           |
| level_id     | int     | Уровень (из `study_level`)             |
| total_words  | int     | Кол-во слов по теме и уровню           |
| learned_words| int     | Сколько выучено                        |
| percent_done | float   | % выполнения темы                      |
| updated_at   | date    | Последний пересчёт                     |

🧠 При повышении `level_id_current`:
- записи по старому уровню удаляются
- создаются записи по новому

---

### 4. level_matrix

Хранит CEFR-логику перехода на следующий уровень.

| Поле              | Тип    | Описание                          |
|-------------------|--------|-----------------------------------|
| level_id_client   | int    | Целевой уровень (1–6)             |
| required_coverage | int    | % охвата (например, 50 или 100)   |
| required_accuracy | int    | % точности (например, 100)        |

🧩 `required_accuracy` задаётся глобально: `LEVEL_ACCURACY_THRESHOLD = 100`

---

## 🛠 Ключевые модули

| Модуль                     | Назначение                                       |
|----------------------------|--------------------------------------------------|
| save_client_activity_log   | логирует ответы, обновляет `learned_words`, `stats` |
| save_client_analytics      | обновляет `rating`, `progress`, `level_id_current` |
| calculate_client_id_current| логика перехода уровня из `level_matrix`        |
| view_user_theme_progress   | агрегированный прогресс по темам                |
| view_personalized_words    | персонализированная выдача слов                 |

---

## ⚙️ Конфигурация проекта

### config.py — Системные настройки:
- ENV_MODE, DEBUG, токены, флаги

### settings.py (config.py) — Пользовательские параметры:
- `LEARN_THRESHOLD = 3`
- `LEVEL_ACCURACY_THRESHOLD = 100`
- `LANGUAGE_TARGET = 'es'`

---

## 📌 Общие требования

- 🔁 Переиспользовать текущую архитектуру: `client_info`, `client_activity_log`, `dictionary`
- 🧩 Все расчёты должны быть прозрачны и масштабируемы
- 📊 Поддержка мультиязычности закладывается через `LANGUAGE_TARGET`