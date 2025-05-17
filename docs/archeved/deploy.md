# ⚙️ Инструкция по развёртыванию и автодеплою Esp2Ru_bot

---

## 📥 Требования

- Python 3.11+ (для локальной разработки)
- Docker + Docker Compose (dля продакшн-развёртывания)
- Ubuntu VPS (Selectel)
- PostgreSQL 15+
- Доступ к GitHub и секретам Actions

---

## 🚀 Развёртывание локально

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/Nikolay08041979/Esp2Rus_bot.git
cd Esp2Rus_bot
```

### 2. Создайте .env

```bash
cp env.example .env
nano .env
```
Заполните параметры:

```dotenv
BOT_TOKEN=ваш_токен
DB_USER=postgres
DB_PASSWORD=пароль
DB_NAME=esp2rus
DB_HOST=localhost
DB_PORT=5432
ADMIN_IDS=ваш_telegram_id
```

### 3. Запуск через Docker

```bash
docker compose up -d --build
```

---

## 🌐 Развёртывание на сервере

### 1. Установка Docker

```bash
apt update && apt install docker.io docker-compose -y
systemctl enable docker
systemctl start docker
```

### 2. Клонирование проекта

```bash
git clone https://github.com/Nikolay08041979/Esp2Rus_bot.git
cd Esp2Rus_bot
```

### 3. Настройка .env для Docker

```dotenv
BOT_TOKEN=ваш_токен
DB_USER=postgres
DB_PASSWORD=пароль
DB_NAME=esp2rus
DB_HOST=db
DB_PORT=5432
ADMIN_IDS=ваш_telegram_id
```

### 4. Запуск Docker

```bash
docker compose up -d --build
```

---

## 🛡️ Автодеплой через GitHub Actions

- Генерируется SSH-ключ
- Приватный ключ загружается в GitHub Secrets
- По каждому push-у в main происходит подключение к серверу
- Выполняются:
  - `git pull origin main`
  - `docker compose up -d --build`

**Workflow:** `.github/workflows/deploy.yml`

---

## 🛠️ Типовые проблемы

| Ошибка | Решение |
|:---|:---|
| Permission denied (publickey) | Проверь корректность приватного и публичного ключа |
| cd: No such file | Неверный путь в workflow |
| Ошибка подключения к БД | Указывай `DB_HOST=db` в докере |

---

# 📆 Готово!

🚀 Теперь бот автоматически обновляется при пуше в main!