## 🧱 Создание таблиц

Для начальной установки используйте скрипт:
```bash
python create_analytics_tables.py
```

Он создаст следующие таблицы:
- `client_info`
- `client_activity_log`
- `client_analytics`
- `study_levels` (справочник CEFR уровней)

---

## 🔄 Миграция старой таблицы уровней языка

Если вы обновляете проект со старой таблицей `study_level`, выполните миграцию.

### 🧪 Пилотный режим (тестовый запуск)
1. Убедитесь, что `PILOT_MODE = True` в:
```python
migrate_study_levels_to_new_table.py
```

2. Запустите:
```bash
python migrate_study_levels_to_new_table.py
```

3. Проверьте лог:
```
data/logs/migration_study_levels.log
```

### 🚀 Полная миграция (удаление старой таблицы)
1. Установите `PILOT_MODE = False` в скрипте.
2. Повторно запустите миграцию:
```bash
python migrate_study_levels_to_new_table.py
```

---

## 📊 Админ-панель и аналитика

Команды:
- `/admin_clients` — общая статистика за период
- `/report` — статистика по конкретному пользователю

Метрики:
- Количество уникальных клиентов
- Количество викторин
- Уровень владения языком
- Динамика прогресса

---

## 🧪 Тесты

Тесты логики и SQL-запросов будут размещены в папке `tests/`.

---

## 📁 Структура проекта

```
core/
  └── config.py
data/
  └── logs/
scripts/
  ├── create_analytics_tables.py
  └── migrate_study_levels_to_new_table.py
```