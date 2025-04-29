![CI Status](https://github.com/Nikolay08041979/Esp2Rus_bot/actions/workflows/python-app.yml/badge.svg)
![Deploy Status](https://github.com/Nikolay08041979/Esp2Rus_bot/actions/workflows/deploy.yml/badge.svg)


# 🇪🇸 Esp2Ru_bot — Telegram-бот для изучения испанского

## Общее описание проекта

**Наименование бота**: @Esp2Rus_bot  
**Цель**: Образовательный Telegram-бот для тренировки перевода испанских слов на русский язык с помощью интерактивных викторин.  
**Референс**: @InMindBot  

---

**⚙️ MVP функциональность**:
- Выбор категории слов и уровня сложности 
- Интерактивная викторина с подсчётом правильных ответов 
- Загрузка слов в базу данных через Telegram (CSV)
- Административная панель внутри бота (/admin)
- Автоматический деплой через GitHub Actions на сервер

---

## Структура базы данных

#### [Описание целевой архитектуры БД проекта](DOCs/db_structure.md)

##### ![Архитектура БД проекта (этап MVP)](DOCs/schema_v1.png)

##### [📄 SQL-скрипт для создания таблиц БД (этап MVP)](db/schema.sql)

---
## 🛠 Стек технологий

- **Язык**: Python 3.11+
- **Фреймворк для бота**: aiogram (v3+)
- **СУБД**: PostgreSQL (через DBeaver)
- **ORM / драйвер БД**: SQLAlchemy
- **Хранилище JSON/CSV**: вручную через Telegram
- **Управление конфигурацией**: .env + dotenv
- **Логика FSM**: встроенная в aiogram FSMContext
- **Инфраструктура и деплой**: Docker + Docker Compose, VPS (Selectel)
- **CI/CD**: GitHub Actions (автоматический деплой)

---

## 📦 Структура проекта

```
Esp2Ru_bot/
├── bot/                # Хендлеры пользователей и админов
├── core/               # Конфигурация, утилиты
├── db/                 # Модели базы данных и импорт слов
├── data/               # Логи, загруженные CSV/JSON файлы
├── scripts/            # Скрипты для аналитики
├── .github/workflows/  # CI/CD пайплайны
├── DOCs/               # Подробная документация проекта
├── main.py             # Точка входа
├── docker-compose.yml  # Сборка через Docker
├── Dockerfile          # Билд образа
├── README.md           # Основной документ

```
## 📜 [Основная документация проекта](DOCs/README.md)

#### 📚 [Детальная структура проекта](DOCs/project_structure.md)
#### 🧪 [Документация по меню и админ-панели](DOCs/admin_panel.md)
#### ⚠️ [Подробные инструкции по автодеплою проекта](DOCs/deploy.md)
#### 🚀 [Roadmap проекта](DOCs/roadmap.md)
#### 🔧 [Исправленные баги](DOCs/bugs.md)


### 📩 Обратная связь: [@nikolay_mazur](https://t.me/nikolay_mazur)