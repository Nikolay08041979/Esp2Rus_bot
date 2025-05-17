
Esp2Rus_bot — Архитектура и требования к персонализации (v2)

Цель:
Построить персональный маршрут обучения для каждого пользователя, в котором:
• Слова считаются выученными при многократном подтверждённом знании
• Прогресс по уровням и темам отслеживается и обновляется автоматически
• Уровень владения языком определяется по охвату и точности
• Повторения регулируются автоматически

---

1. Таблица: learned_words

Поля:
- client_id (int) — ID пользователя (из client_info)
- word_id (int) — ID слова (из dictionary)
- learned_at (date) — Дата выучивания слова
- activity_id (int) — Ссылка на сессию (из client_activity_log)

Логика:
- Слово считается выученным после N правильных ответов
- Значение N задаётся в параметре LEARN_THRESHOLD
  • По умолчанию LEARN_THRESHOLD = 3
  • Хранится в settings.py

---

2. Таблица: user_word_stats

Поля:
- client_id (int) — ID пользователя (из client_info)
- word_id (int) — ID слова (из dictionary)
- total_seen (int) — Сколько раз слово показывалось
- correct (int) — Сколько раз пользователь ответил правильно
- incorrect (int) — Количество ошибок
- last_seen (date) — Последний показ слова

---

3. Таблица: user_progress_by_theme

Цель: оперативно предоставлять детализированный и агрегированный прогресс по темам и уровню.

Поля:
- client_id (int) — ID пользователя (из client_info)
- cat_id (int) — ID темы (из word_category)
- level_id (int) — Текущий уровень пользователя (lev_id из study_level)
- total_words (int) — Общее количество слов в теме (из dictionary)
- learned_words (int) — Количество выученных слов
- percent_done (float) — Процент завершения темы
- updated_at (date) — Последний пересчёт

Источники данных:
- dictionary (по cat_id и lev_id)
- learned_words (связь по word_id)

Важно:
- В таблице хранится только один активный уровень на пользователя
- При повышении уровня (level_id_current в client_analytics):
  • записи по предыдущему уровню удаляются
  • создаются новые записи по всем темам нового уровня

---

4. Таблица: level_matrix

Назначение: гибкая логика расчёта уровня владения (level_id_current)

Поля:
- level_id_client — целевой уровень (1 — A1, ..., 6 — C2), мэппится на level_id и level_client (из study_levels)
- required_coverage — минимальный % выученных слов (50 или 100)
- required_accuracy — точность ответов

Правила:
- required_accuracy задаётся глобально через параметр LEVEL_ACCURACY_THRESHOLD = 100 (в settings.py)
- level_matrix управляется через таблицу в БД (editable)

---

Ключевые модули и действия:
- save_client_activity_log.py — обновляет user_word_stats и learned_words
- save_client_analytics.py — обновляет client_rating, user_progress_by_theme, level_id_current
- calculate_client_id_current.py — логика присвоения уровня из матрицы
- cron-задача — для автообновления client_analytics
- view_user_theme_progress — для быстрой выборки по темам
- view_personalized_words — при формировании сессии

---

Файл config.py — содержит:
• Системные настройки проекта (режимы, API ключи, флаги окружения)

Файл settings.py — содержит:
• Пользовательские параметры:
  • LEARN_THRESHOLD = 3
  • LEVEL_ACCURACY_THRESHOLD = 100
  • Язык изучения (LANGUAGE_TARGET = 'es')

---

Общее требование:
🔁 Максимально переиспользовать уже созданную архитектуру БД, таблицы, индексы и view
