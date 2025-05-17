# 📊 Техническое задание: Аналитика Esp2Rus_bot (v2)

## 🎯 Цель:
Создание масштабируемого, модульного и устойчивого аналитического стека, который позволяет:
- отслеживать активность пользователей Telegram-бота
- рассчитывать ключевые метрики (`quiz_weight`, `client_rating`)
- строить персонализированные маршруты обучения
- автоматизировать отчётность и валидацию

---

## 📁 Структура проекта

```
analytics/
├── analytics.py                         # orchestration layer
├── save_client_activity_log.py          # запись client_activity_log + client_activity_words
├── save_client_analytics.py             # расчёт client_rating + уровень
├── rollback_analytics.py                # откат
├── personalization/
│   ├── update_learned_words.py
│   ├── update_user_progress_by_theme.py
│   └── ...
├── reports/
│   ├── report_user.py                   # /report @user
│   ├── summary_cron.py                  # cron-аналитика
│   └── forms/
│       ├── csv_template_user_report.csv
│       └── ...
├── metrics/
│   ├── calculate_quiz_weight.py
│   ├── calculate_client_rating.py
│   ├── get_level_id_word.py
│   ├── calculate_level_current.py
│   └── ...
```

---

## 📐 Метрики

| Метрика           | Источник/Логика                                     |
|-------------------|-----------------------------------------------------|
| `quiz_weight`     | Средний вес слов викторины через `view_word_weight` |
| `client_rating`   | Сумма `quiz_weight` всех успешных сессий            |
| `level_id_word`   | Уровень слов — `get_level_id_word()`                |
| `level_id_current`| Покрытие + точность через `calculate_level_current`|

---

## 🔁 Логирование

- `data/logs/analytics_debug/*.log`
- `cron_events` (PostgreSQL) — системные задачи

---

## ⚙️ Управление

- `USE_ANALYTICS_V2 = True` — включение нового стека
- `DELETE_INACTIVE_CLIENTS = False` — удаление временных клиентов через 24 часа
- `LEVEL_CALCULATION_ONLINE = True` — расчет уровня после каждой викторины
- `rollback_analytics.py` — отключение + восстановление `analytics_v1`

---

## 📊 База данных

| Таблица                     | Назначение                                              |
|-----------------------------|----------------------------------------------------------|
| `client_info`               | Базовая информация по пользователю                      |
| `client_activity_log`       | Лог сессий викторины                                    |
| `client_activity_words`     | Слова, входившие в сессию                               |
| `client_analytics`          | Производные метрики (rating, level, score_total и т.п.) |
| `learned_words`             | Выученные слова (≥3 успешных повторов)                 |
| `user_word_stats`           | Статистика по каждому слову (в разработке)              |
| `user_progress_by_theme`    | Прогресс по темам и уровням (для UI и отчётности)       |
| `study_levels`              | CEFR-структура уровней сложности                        |
| `level_matrix`              | Матрица условий перехода между уровнями                 |

---

## 📆 Этапы релиза

### Этап 1. Подготовка — ✅
- Структура каталогов и баз данных
- Скрипты аналитики, логирования, расчёта метрик

### Этап 2. Интеграция в Telegram-бот — ✅
- asyncpg
- сбор статистики quiz
- запись client_info, client_analytics

### Этап 3. Валидация и отладка — ✅
- Юнит-тесты
- сравнение с прошлой версией
- проверка quiz_weight, learned_words, rating

### Этап 4. Мониторинг и откат — ✅
- rollback_analytics.py
- cron_events
- config-флаги

---

## 🔜 Следующие этапы:

### Этап 5. Персонализация — 🟡
- `user_progress_by_theme` — обновление при викторине
- `user_word_stats` — расчёт или архив
- `client_level_progress` — готов как VIEW

### Этап 6. Панель и отчётность — 🟡
- `/admin_clients`
- `/report @user`
- `analytics/reports/report_user.py`

### Этап 7. Cron-аналитика — 🔜
- `summary_cron.py`: активность, динамика, рейтинг

### Этап 8. Миграция в прод — 🔜
- `run_install.py`
- `README_Prod_Migration.md`
- автоустановка VIEW и таблиц