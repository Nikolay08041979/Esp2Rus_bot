
# 📊 Esp2Rus_bot — Аналитический стек v2

## 🚀 Назначение
Аналитический стек v2 предназначен для более точного расчёта метрик пользователей:
- `quiz_weight` — динамический вес викторины по сложности слов
- `client_rating` — накопленный рейтинг клиента
- `level_id_current` — (в будущем) текущий уровень пользователя по CEFR

## 🧪 Этап 2: Staging

### ✅ Включение нового стека
Установите в `core/config.py`:
```python
USE_ANALYTICS_V2 = True
```

### 🧱 Файл логики
Замените:
```
analytics.py ← analytics_v2_logging_fixed.py
```

### 📂 Логирование
Все метрики логируются в:
```
data/logs/analytics_debug/quiz_weight_v2.log
```
**Пример записи:**
```
2025-05-09 14:30:24: client_id=1, quiz_weight=1.1, client_rating=58.03
```

### 📌 Проверки:
- `client_activity_log` — запись сессии
- `client_analytics` — обновление итоговых метрик
- `quiz_weight` пересчитан по `view_word_weight`
- `client_rating` накапливает сумму `quiz_weight` за все викторины

---

## 🛑 Возможность отката
Флаг `USE_ANALYTICS_V2 = False` вернёт старую аналитику.

## 🔜 В разработке:
- Автоматический расчёт `level_id_current`
- Фоновая синхронизация `sync_client_analytics.py`
- Ежедневный cron + логирование в `cron_events`
