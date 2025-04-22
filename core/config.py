import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Automatically switch DB_HOST based on environment
# Set DEBUG=1 in your .env file for local development
if os.getenv("DEBUG", "0") == "1":
    DB_HOST = "localhost"
else:
    DB_HOST = "db"

DB = {
    "user": os.getenv("DB_USER"),            # имя пользователя БД
    "password": os.getenv("DB_PASSWORD"),    # пароль от БД
    "database": os.getenv("DB_NAME"),        # название базы
    "host": os.getenv("DB_HOST"),            # хост, например, "localhost" или "db"
    "port": int(os.getenv("DB_PORT")),       # порт PostgreSQL, по умолчанию 5432
}

admin_raw = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = [int(x.strip()) for x in admin_raw.split(",") if x.strip().isdigit()]

