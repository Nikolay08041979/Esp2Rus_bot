# 📦 Подробная структура проекта

```
esp2rus_bot/
├── bot/
│   ├── __init__.py
│   ├── handlers/                 
│   │   ├── __init__.py
│   │   ├── user_handlers.py      # Логика викторины: обработка команд /start, /help и логика для пользователей
│   │   └── admin_handlers.py     # Админ панель: загрузка CSV-файлов, добавление и удаление категорий и уровней
│   ├── states/
│   │   ├── __init__.py           # FSM-состояния  
│   │   ├── adnin_states.py       # FSM-состояния для админ панели
│   ├── keyboards.py              # клавиатуры Telegram
│
├── core/
│   ├── __init__.py
│   ├── config.py                 # Конфиги: токен, список админов, пути
│   ├── file_utils.py             # Вспомогательные функции: валидация, рандомизация
│   └── converter.py              # CSV → JSON (сохраняет words.json)
│
├── db/
│   ├── __init__.py
│   ├── models.py                 # SQLAlchemy-модели
│   ├── schema_legacy.sql/png            # SQL-структура БД / схема БД
│   └── importer.py               # Импорт JSON в БД
│
├── data/
│   ├── uploads                   # сюда складывать все загруженные CSV и их конвертации в JSON
│   ├── logs                      # сюда сохранять JSON с добавленными словами
│   ├── errors                    # сюда сохранять JSON с ошибками при импорте
│
├── scripts/
│   └── stats.sql                 # Готовые SQL-скрипты для подсчет аналитики в разных разрезах
│
├── DOCs/                         # Подробная документация проекта
│
├── .github/workflows/            # CI/CD пайплайны
│── .gitignore                    # Исключение виртуального окружения
├── .env                          # ТГ Токен и учетные данные для подключения к БД 
├── .env.example                  # шаблон окружения
├── docker-compose.yml            # Сборка через Docker
├── Dockerfile                    # Билд образа
├── requirements.txt              # Зависимости проекта
├── README.md                     # Текущий документ
├── main.py                       # Точка входа: регистрация хендлеров, запуск бота
