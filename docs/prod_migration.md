### 📦 Esp2Ru Bot — Миграция на продакшн (v2.0)

### 1. Технические предусловия

* Python 3.10+
* PostgreSQL 14+
* Docker + docker-compose (опционально)
* .env файл c переменными среды (`BOT_TOKEN`, `DB settings`, `ENV_MODE`, и др.)

---

### 2. Подготовка до релиза:

### Создание бэкапа критичепски важных данных на сервере:

Бэкап **обязательно** создаётся перед запуском `run_install.py` или деплоем новой версии.

Список ключевых таблиц:

1. `client_info`  
2. `client_analytics`  
3. `dictionary`  
4. `word_category`  
5. `study_level`  
6. `study_levels`  
7. `learned_words`  

```bash
pg_dump -U <DB_USER> -h <DB_HOST> -d <DB_NAME> \              
  -t client_info \
  -t client_analytics \
  -t dictionary \
  -t word_category \
  -t study_level \
  -t study_levels \
  -t learned_words \
  > backup_7_tables.sql
```

### 📦 Заморозка зависимостей проекта на локальной машине:

После установки всех библиотек и проверки работы проекта зафиксируйте зависимости:

```bash
pip freeze > requirements.txt
```

### Добавление всех данных на GitGub, прикрепление к релизу:

```bash
git add .
git commit -m "Add all data"
git push
```

`git checkout release-v3.0.0`

Мы будем делать клонирование данных с GitHub или запускаться через github actions?

## 3. Подготовка на сервере:

- Убедись, что `.env` содержит корректные параметры подключения к прод-базе
- В корне проекта должен находиться файл `backup_7_tables.sql`
- Обнови зависимости: `pip install -r requirements.txt`
- Проверь, что директория `data/logs/` существует
- Проверь конфигурационные флаги в `.env` или config.py:
```python
DELETE_INACTIVE_CLIENTS = False
LEVEL_CALCULATION_ONLINE = True
ENABLE_AUTO_REPORTS = True
ENABLE_DROP_TABLES = True
ENABLE_RESTORE_DATA = True

```

## 4. Стартовая инсталляция

Скрипт `run_install.py` выполняет:

1. Удаление 7 таблиц, восстановленных из дампа
2. Восстановление данных из `backup_7_tables.sql`
3. Создание всех остальных таблиц (например, `client_activity_log`, `cron_events`, `user_word_stats`)
4. Создание всех VIEW:
   - `study_level_mapped`
   - `level_matrix`
   - `quiz_weight_by_group`
   - `client_level_progress`
   - `user_progress_by_theme`
   - `personalized_words`
   - `word_success_count`
   - `word_weight`
5. Пост-проверку:
   - соответствие `client_id` между `client_analytics` и `client_info`
   - заполненность `level_id_current`
6. Отправку уведомления администраторам в Telegram (при наличии `ADMIN_IDS`)
7. По флагу `--sync`: запуск `run_sync_all_clients_with_tg_notify.py`, который:
   - проверяет заполненность ключевых таблиц
   - обновляет VIEW'шки
   - пересоздаёт `user_progress_by_theme` через `TRUNCATE + INSERT`

---
Команда запуска
```bash
python run_install.py --sync
```
Флаг `--sync` запускает скрипт `run_sync_all_clients_with_tg_notify.py` после всех шагов установки.

---


### 5. Деплой через GitHub Actions (CI/CD) 

#### 🛠️ Подготовка:
* SSH-доступ на прод-сервер настроен (добавлен публичный ключ).
* В GitHub добавлены secrets: `SSH_PRIVATE_KEY, REMOTE_HOST, REMOTE_USER, REMOTE_DIR`
* Файл [deploy.yml](.github/workflows/deploy.yml) добавлен в репозиторий

#### 🛡️ Проверка после деплоя
* Убедитесь, что бот успешно стартует (/start)
* Проверьте логи (Docker, systemctl, таблица cron_events)
* Выполните admin/report и проверьте прогресс


### 6. Крон-задачи (cronjobs)

* Ежедневно в 00:01:

  * `sync_client_analytics.py` — расчёт client_rating и level_id_current (если LEVEL_CALCULATION_ONLINE = False)
  * `generate_admin_day_report.py` — агрегированный отчёт по пользователям
* Планируемое размещение: crontab / systemd / Docker cron


### 7. Отчёты и логи

* `/admin/report` — агрегированный отчет
* `/admin/report/<tg_id>` — индивидуальный отчет
* `/admin/report/log` и `/admin/report/log/N` — логи cron-задач за период
* Все логи в таблице `cron_events`

---

## 8. Проверка состояния

- Все шаги логируются в файл:
  ```
  data/logs/run_install.log
  ```
- Ошибки и действия внутри `--sync` логируются в:
  ```
  data/logs/sync_client_analytics.log
  ```
- В Telegram отправляется краткое уведомление администраторам

---

## 9. Telegram-уведомление администраторам

Если `.env` содержит `BOT_TOKEN` и `ADMIN_IDS`, по завершении установки отправляется уведомление:

**Успешно:**
```
🧾 РЕЗУЛЬТАТ УСТАНОВКИ:
✅ Установка завершена без ошибок.
```

**С ошибками:**
```
🧾 РЕЗУЛЬТАТ УСТАНОВКИ:
⚠️ Установка завершена с ошибками:
  - Ошибка создания user_progress_by_theme.sql
  - Найдено 2 записи без level_id_current
```

---

## 10. Ручное восстановление при необходимости

```bash
psql -U postgres -h localhost -d esp2rus_v2dev -f backup_7_tables.sql 
```


### 11. 🚨 Rollback-план: как откатить релиз

Если после релиза обнаружены критические ошибки, которые невозможно оперативно устранить:

#### 📍 Остановить текущую сборку

```bash
# Если используется systemd
sudo systemctl stop esp2ru_bot

# Или через Docker
docker-compose down
```

#### 📍 Восстановить стабильную версию `v2.0.0`

Перед загрузкой новой сборки убедитесь, что сохранены:
- `dump_before_update.sql` — SQL-дамп базы (`pg_dump`)
- `requirements_v2.0.0.txt` — зависимости на момент публикации v2.0.0
- Исходники: [GitHub Release v2.0.0](https://github.com/Nikolay08041979/Esp2Rus_bot/tree/v.2.0.0)

Шаги отката:

```bash
psql -U <user> -d <db> -f dump_before_update.sql
git checkout v2.0.0
pip install -r requirements_v2.0.0.txt
```

#### 📍 Проверить работоспособность

- Запустить бота
- Проверить команды `/start`, `/admin`, `/report`
- Убедиться в отсутствии ошибок в логах (`cron_events`, консоль, Telegram`)
#### 📍 1. Остановить новый релиз

```bash
# Если используется systemd
sudo systemctl stop esp2ru_bot

# Или через Docker
docker-compose down
```

### 8. Сопутствующие документы

* [admin_manual.md](admin_manual.md)
* [README_release_v2.md](release_v2.md)
* [architecture.md](architecture.md)
* [troubleshooting.md](troubleshooting.md)