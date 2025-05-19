# 📘 Esp2Rus\_bot — Telegram-бот для изучения испанского

Esp2Rus\_bot — это асинхронный Telegram-бот на базе Python + PostgreSQL для тренировки испанских слов с адаптивной логикой на основе CEFR-уровней.

## 🚀 Возможности

* 🎯 Адаптивная система сложности: A1 → C2 по CEFR
* 📚 Автоматическая персонализация слов: исключает выученные
* 🧠 Аналитика прогресса, рейтинг, уровни и отчёты
* 🛠 Админ-панель: отчёты, CSV-логи, статистика пользователей
* ⚖️ Умный расчёт сложности викторины (quiz_weight), основанный на уровне и количестве слов


## 📦 Основные компоненты

* `bot/` — FSM-логика, роутеры и интерфейс Telegram
* `analytics/` — аналитика прогресса, рейтинги, метрики, cron
* `db/` — SQL-таблицы, VIEW, миграции
* `docs/` — вся документация (релиз, миграции, админка и т.д.)

## 🧪 Запуск (dev)

```bash
# Клонируем и переходим в проект
git clone https://github.com/username/Esp2Rus_bot.git
cd Esp2Rus_bot

# Устанавливаем зависимости
pip install -r requirements.txt

# Запускаем бота
python main.py
```

## 🧩 Дополнительные материалы

* [🔍 CEFR логика и аналитика v2](/docs/release_v2.md)
* [📦 Миграция на прод](docs/prod_migration.md)
* [🛠 Админ-команды и шаблоны](docs/admin_manual.md)
* [⚙️ Архитектура и взаимодействие модулей](docs/architecture.md)
* [🐛 Отладка и FAQ](docs/troubleshooting.md)

## 💡 Контрибьютинг

Хочешь присоединиться? Прочитай [CONTRIBUTING.md](docs/contributing.md) и [issue tracker](https://github.com/username/Esp2Rus_bot/issues).

---

© 2025 Nikolay Mazur
