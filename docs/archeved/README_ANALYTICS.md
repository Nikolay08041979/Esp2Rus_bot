# Установка клиентской аналитики Esp2Rus_bot (Этап 1)

Этот модуль предназначен для первичной установки и валидации клиентской аналитики бота.

## 📦 Что делает `run_install.py`:
1. Делает бэкап и удаляет старые клиентские таблицы
2. Создаёт таблицы:
   - `study_levels`
   - `client_info`
   - `client_activity_log`
   - `client_analytics`
3. Проверяет соответствие `lev_name = level_word`
4. Создаёт представление `view_study_level_mapped` для наглядной связи

---

## Структура базы данных

##### ![Архитектура БД проекта (этап MVP)](images/schema_v2.png)

---


---

## 🚀 Как запустить

> Убедись, что у тебя корректно настроен `.env` файл с параметрами БД

```bash
python run_install.py
```

---

## 📁 Структура

```
install/
│
├── run_install.py                ← основной модуль запуска
│
├── steps/
│   ├── step1_drop_and_backup.py       ← безопасное удаление таблиц
│   ├── step2_create_tables.py         ← создание новых таблиц
│   ├── step3_verify_links.py          ← soft-связи
│   ├── step4_create_view.py           ← создание view
│   └── step5_done.py                  ← финальный вывод
│
├── logs/                       ← все логи по шагам
└── backup/sql/                 ← дампы удалённых таблиц


Esp2Ru_bot/
│
├── bot/                         ← Telegram-бот, FSM, хендлеры
│   ├── handlers/
│   ├── states/
│   └── keyboards/
│
├── core/                        ← Конфиги, утилиты, ENV
│   └── config.py
│
├── db/                          ← Всё, что связано с БД
│   ├── migrations/              ← Скрипты миграции и фоновые обновления
│   │   └── update_client_levels.py      ← Обновление level_id_current из VIEW
│   ├── create_tables/           ← Создание всех таблиц
│   ├── views/                   ← SQL-представления (VIEWs)
│   ├── sql/                     ← Файл client_analytics.sql (все аналитические SELECT-запросы)
│   └── utils.py                 ← Общие функции (get_conn, run_query и т.п.)
│
├── analytics/                  ← Модули аналитики
│   ├── db_analytics.py         ← Асинхронная логика записи
│   └── metrics/                ← Метрики, расчёты рейтинга
│
├── cronjobs/                   ← Автообновления (в т.ч. bash-скрипты)
│   └── run_daily_updates.sh    ← Ежедневное обновление уровней
│
├── install/                    ← Модуль первого развёртывания
│   ├── run_install.py
│   └── steps/
│       ├── step1_drop_and_backup.py
│       ├── step2_create_tables.py
│       ├── step3_verify_links.py
│       ├── step4_create_view.py
│       └── step5_done.py
│
├── logs/
│   └── cron/
│       └── level_update_YYYYMMDD.log
│
├── backup/
│   └── sql/                     ← Дампы таблиц по дате
│
├── README.md
└── README_ANALYTICS_STAGE_1.md

Esp2Ru_bot/
│
├── bot/                         # FSM, хендлеры и Telegram-логика
│   └── handlers/, states/, keyboards/
│
├── core/                        # Конфигурации и утилиты
│   └── config.py, ...
│
├── analytics/                  # Подсчёты, запись, бизнес-логика аналитики
│   └── db_analytics.py, metrics/
│
├── cronjobs/                   # Автозапуски, фоновые обновления
│   └── run_daily_updates.sh
│
├── install/                    # Шаги установки и инициализации
│   └── steps/
│       ├── step1_drop_and_backup.py
│       ├── ...
│
├── db/                         # Технические и системные SQL/миграции
│   ├── migrations/
│   │   └── update_client_levels.py
│   ├── create_tables/
│   ├── views/
│   └── sql/
│
├── data/                       # ВСЕ ДАННЫЕ ПРОЕКТА
│   ├── logs/
│   │   ├── cron/
│   │   │   └── level_update_YYYYMMDD.log
│   │   └── import_log_*.json
│   ├── backup/
│   │   └── sql/                      # Дампы удалённых таблиц
│   ├── uploads/                     # Файлы для загрузки (CSV, JSON и т.д.)
│   ├── json/                        # Генерируемые JSON-ответы, raw-данные
│   ├── errors/                      # Логи/дампы ошибок (если будут)
│   └── export/                      # Готовые выгрузки, если появятся
│
├── README.md
└── README_ANALYTICS_STAGE_3.md

analytics/
├── analytics.py                           # 🎯 Главный координатор (опц.) — orchestration layer
├── save_client_activity_log.py            # 💾 Сохраняет сессию в client_activity_log и client_activity_words
├── save_client_analytics.py               # 📊 Агрегирует клиентские метрики и сохраняет в client_analytics
└── metrics/                               # 📐 Все расчётные модули
    ├── calculate_client_rating.py         # 🔢 Считает client_rating = Σ quiz_weight
    ├── calculate_level_id_current.py      # 🧠 Считает текущий CEFR-уровень клиента
    ├── calculate_quiz_weight.py           # ⚖️  Считает quiz_weight по словам
    └── ...


```
| Этап    | Скрипт                               | Назначение                                                                                                             |
| ------- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| **1.0** | `step1_backup_and_cleanup.py`        | Бэкап и (опциональное) удаление всех таблиц, включая `esp2rus_dictionary`, `study_level`, `word_category` и клиентские |
| **1.1** | `step1_1_backup_and_cleanup_dict.py` | Отдельный бэкап и удаление только словаря                                                                              |
| **2.0** | `step2_create_tables.py`             | Создание таблиц `study_levels`, `client_info`, `client_analytics`, `client_activity_log`                               |
| **2.1** | `step2_1_create_dict_tables.py`      | Создание `esp2rus_dictionary`, `study_level`, `word_category`                                                          |
| **3.0** | `step3_restore_from_backup.py`       | Восстановление данных из последнего бэкапа во все таблицы                                                              |
| **4.0** | `step4_verify_links.py`              | Верификация связей `study_level ↔ study_levels`                                                                        |
| **5.0** | `step5_create_view.py`               | Создание `VIEW` (`view_study_level_mapped`, `client_level_view`, ...)                                                  |
| **6.0** | `step6_finalize.py`                  | Финальный лог установки и завершение                                                                                   |
| **7.0** | `step7_prod_backup.py` (cron-only)   | После установки остаётся только ежедневный бэкап (`client_info_latest.sql`, `dictionary_latest.sql`) с перезаписью     |

| Шаг | Скрипт                               |
| --- | ------------------------------------ |
| 1.0 | `step1_backup_and_cleanup.py`        |
| 1.1 | `step1_1_backup_and_cleanup_dict.py` |
| 2.0 | `step2_create_tables.py`             |
| 2.1 | `step2_1_create_dict_tables.py`      |
| 3.0 | `step3_restore_from_backup.py`       |
| 4.0 | `step4_verify_links.py`              |
| 5.0 | `step5_create_view.py`               |
| 6.0 | `step6_finalize.py`                  |
| 7.0 | `step7_prod_backup.py`               |
|     | `run_install.py`                     |

---

## 📌 Логи

Все логи установки сохраняются в:  
`/backup/logs/`

---

## 🧠 Рекомендация

После установки — зайти в DBeaver и проверить представление `view_study_level_mapped` вручную.

---

**Подготовлено:** 2025-05-04  
**Автор:** Мазур Николай 
