
# ⚙️ Esp2Rus_bot — Техническое задание: Универсальный установщик БД (Installer Engine)

## 🎯 Цель:
Создать единый механизм управления структурой базы данных (create/replace), который позволяет:
- быстро создавать и пересоздавать таблицы и представления
- централизованно управлять списком объектов
- минимизировать ручное создание файлов .py на каждую таблицу

---

## 📁 Структура проекта

```
db/
├── create/                        # Храним SQL-файлы
│   ├── create_table_client_info.sql
│   ├── create_table_learned_words.sql
│   ├── create_view_user_progress_by_theme.sql
│   └── ...
├── install_config.py              # Описывает, что установить
├── run_install.py                 # Основной управляющий скрипт
```

---

## 📄 install_config.py

```python
INSTALL_SCHEMA = {
    "tables": [
        "client_info",
        "client_activity_log",
        "learned_words",
        ...
    ],
    "views": [
        "view_user_progress_by_theme",
        "view_personalized_words"
    ]
}
```

---

## 🛠 Логика работы run_install.py

1. Загружает список объектов из `install_config.py`
2. Для каждой таблицы:
   - Проверяет наличие в БД
   - Делаeт архив таблицы (`CREATE TABLE backup_<name> AS SELECT * FROM <name>`)
   - Удаляет текущую таблицу (`DROP TABLE IF EXISTS ... CASCADE`)
   - Выполняет SQL из файла `create/create_table_<name>.sql`
3. Для каждого VIEW:
   - Удаляет текущее представление (`DROP VIEW IF EXISTS ...`)
   - Выполняет SQL из файла `create/create_view_<name>.sql`
4. Ведёт лог по каждому шагу

---

## ✅ Преимущества:

- ❌ Не нужно вручную писать `create_*.py` для каждой таблицы
- ✅ Унифицированная структура и масштабируемость
- ✅ Удобное добавление новых таблиц в будущем (через SQL + config)
- ✅ Совместимость с текущим `run_install.py` (адаптируем)

---

## 📦 Поток разработки

1. Создаёшь SQL-файл в папке `create/` (тестируешь сначала в DBeaver)
2. Добавляешь имя таблицы/view в `install_config.py`
3. Запускаешь `run_install.py`
4. Всё создаётся и логируется автоматически

---

## 🔐 Требования:

- Полная поддержка PostgreSQL
- Минимальные зависимости (asyncpg + os)
- Логика должна быть идемпотентной (многократные перезапуски = безопасны)

---

