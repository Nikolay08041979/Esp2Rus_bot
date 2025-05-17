
# 📊 Esp2Rus_bot — Финальная архитектура аналитики v2

## ✅ Цель
Новая архитектура аналитики v2 заменяет устаревший стек и обеспечивает:
- Чистую модульную структуру
- Расчёт метрик: quiz_weight, client_rating
- Надёжную запись активности пользователя
- Упрощённое логирование и откат

---

## 📁 Структура

```
analytics/
├── analytics.py                    # orchestration layer
├── save_client_activity_log.py     # запись client_activity_log
├── save_client_analytics.py        # расчёт client_rating
├── metrics/
│   ├── calculate_quiz_weight.py    # формула и fetch
│   ├── calculate_client_rating.py
│   ├── get_level_id_word.py
│   └── ...
```

---

## 📐 Метрики

| Метрика           | Описание                                      |
|-------------------|-----------------------------------------------|
| `quiz_weight`     | Средний вес слов викторины через view         |
| `client_rating`   | Сумма `quiz_weight` всех 100% сессий          |
| `level_id_word`   | Уровень слов — из таблицы `study_levels`      |
| `level_id_current`| ❌ не реализован, зарезервирован               |

---

## 🧪 Работа логики

1. Пользователь проходит викторину
2. `analytics.py` вызывает:
   - `save_client_activity_log(data)`
   - `save_client_analytics(client_id)`
3. В лог (`data/logs/analytics_debug/quiz_weight_v2.log`) пишется:
```
2025-05-09 18:40:55: client_id=1, quiz_weight=1.1, client_rating=62.43
```
4. Запись также логируется в таблицу `cron_events`

---

## 🔁 Откат

Используйте:
```
python tools/rollback_analytics.py
```

Действия:
- Меняет флаг `USE_ANALYTICS_V2 = False`
- Восстанавливает `analytics.py` из `analytics_old/analytics_v1_backup.py`

---

## 🧾 Логирование

| Источник               | Путь/таблица                                |
|------------------------|----------------------------------------------|
| Сессии                 | `data/logs/analytics_debug/quiz_weight_v2.log` |
| Ошибки/события cron    | таблица `cron_events` в PostgreSQL           |

---

## 🛡 Надёжность

- Вся логика работает асинхронно (asyncpg)
- Устойчиво к отсутствию данных (fallback = None)
- Поддерживает rollback и версионирование

---

## 🧭 В планах

- Персонализация и `level_id_current`
- Подключение `/my_stats` в Telegram
- CI/CD + pytest для метрик
