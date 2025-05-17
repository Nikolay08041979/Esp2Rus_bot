import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# === Определение среды ===
ENV_MODE = os.getenv("ENV_MODE", "prod")
DEBUG = os.getenv("DEBUG", "0") == "1"

# === Telegram Bot ===
BOT_TOKEN = os.getenv("BOT_TOKEN_DEV") if ENV_MODE == "dev" else os.getenv("BOT_TOKEN_PROD")

# === PostgreSQL ===
DB = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME_DEV") if ENV_MODE == "dev" else os.getenv("DB_NAME_PROD"),
    "host": "localhost" if DEBUG else os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432))
}

# === Администраторы ===
admin_raw = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = [int(x.strip()) for x in admin_raw.split(",") if x.strip().isdigit()]

# === Пути проекта ===
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
BACKUP_DIR = DATA_DIR / "backup" / "sql"
LOGS_DIR = DATA_DIR / "logs"
EXPORTS_DIR = DATA_DIR / "exports"
CRON_SCRIPTS_DIR = BASE_DIR / "cronjobs"
ERRORS_DIR = DATA_DIR / "errors"
...


# === Публичные проектные настройки ===
LEARN_THRESHOLD = int(os.getenv("LEARN_THRESHOLD", 3))
LANGUAGE_TARGET = os.getenv("LANGUAGE_TARGET", "es")  # es | en | de и т.д.
LANGUAGE_FLAGS = {
    "es": "🇪🇸",
    "en": "🇬🇧",
    "de": "🇩🇪",
    "fr": "🇫🇷",
    "it": "🇮🇹",
    "pt": "🇵🇹",
    "tr": "🇹🇷",
}
flag = LANGUAGE_FLAGS.get(LANGUAGE_TARGET.lower(), "🏳️")


# === Флаги ===
USE_ANALYTICS_V2 = os.getenv("USE_ANALYTICS_V2", "False").lower() == "true"
DELETE_INACTIVE_CLIENTS = False  # по умолчанию удаление клиентов отключено. Для включения режима удаления неактивных клиентов через 24 часа - True
LEVEL_CALCULATION_ONLINE = True  # По умолчанию включён online расчет - True. для переключения на offline-расчёт раз в сутки - False
ENABLE_AUTO_REPORTS = True  # По умолчанию включён автоматическая отправка отчётов - True. для отключения - False. Автоотчет отправляется в 00:01 мск каждого дня за предыдущий день

ENABLE_DROP_TABLES = True
ENABLE_RESTORE_DATA = True # данные будут востановлены только из этих 7 таблиц: client_info, client_analytics, dictionary, word_category, study_level, study_levels, learned_words

