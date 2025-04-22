## ⚙️ Развёртывание проекта: локально и на сервере

> ВАЖНО: проект поддерживает запуск **локально** (для разработки) и на **сервере/VPS** (в Docker-контейнере). Ниже перечислены настройки и переменные, которые **нужно контролировать вручную** для стабильной работы.

---

### 📍 1. Переменная `DB_HOST` в `.env`

- **Локально**:
  ```env
  DB_HOST=localhost
  ```

- **На сервере (в Docker)**:
  ```env
  DB_HOST=db  # имя контейнера с PostgreSQL в docker-compose.yml
  ```

---

### 📍 2. Локальный импорт вручную (не используется в продакшне)

- Скрипты `import_words.py`, `run_import.py` — **нужны только для локального теста**.
- В продакшене весь импорт CSV осуществляется **через Telegram-бота**.

---

### 📍 3. Пример `.env` файла для ЛОКАЛЬНОЙ разработки

```env
# === Telegram Bot ===
BOT_TOKEN=your_bot_token

# === PostgreSQL ===
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=esp2rus
DB_HOST=localhost
DB_PORT=5432

ADMIN_IDS=123456789
```

---

### 📍 4. Пример `.env` файла для ПРОДАКШНА (Docker)

```env
# === Telegram Bot ===
BOT_TOKEN=your_bot_token

# === PostgreSQL ===
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=esp2rus
DB_HOST=db
DB_PORT=5432

ADMIN_IDS=123456789
```

---

### 📍 5. Частые ошибки при переключении между режимами

| Ошибка | Возможная причина |
|--------|--------------------|
| `could not translate host name "db"` | Указан `DB_HOST=db` при локальном запуске (должно быть `localhost`) |
| `connection refused` | PostgreSQL не запущен или порт недоступен |
| `SyntaxError: passing state=` | Используются старые фильтры aiogram (2.x синтаксис), должен быть 3.x |
| `file not found` | Файл `.env` не создан или не скопирован из `.env.example` |

---

### 6. Совместимость локальной и серверной среды

- Используется aiogram версии 3.x.
- Вместо `state="..."` используйте `StateFilter(...)`.
- Файл `.env` должен быть настроен отдельно под каждую среду (локальную и серверную).

---

### 📍 7. Отладка проблем

Если при нажатии на `/admin` или `/cancel` начинается викторина:
- Убедись, что `@router.message(Command("cancel"))` и `@router.message(Command("admin"))` находятся **выше** `@router.message(F.text)` в файле `user_handlers.py`

Если не обрабатывается CSV-файл:
- Проверь, что хендлер `@router.message(F.document)` находится **выше всех других message-хендлеров**
- Убедись, что `admin_handlers.py` корректно импортирован в `main.py`

Если нет реакции на `/start`:
- Проверь, что бот не находится в каком-либо `FSMContext`. Команда `/cancel` должна очищать состояние.
