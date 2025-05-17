# 🔁 Финальная синхронизация представлений и логгирование состояния таблиц
import asyncio
import asyncpg
from datetime import datetime
from pathlib import Path
from core.config import DB
from core.config import LOGS_DIR
from analytics.metrics.refresh_user_progress_by_theme import refresh_user_progress

LOG_FILE = LOGS_DIR / "sync_client_analytics.log"


def log(msg: str):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{timestamp} {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

async def refresh_views(conn, errors: list):
    views = [
        "view_client_level_progress",
        "view_user_progress_by_theme"
    ]
    for view in views:
        try:
            await conn.execute(f"REFRESH MATERIALIZED VIEW CONCURRENTLY {view};")
            log(f"[OK] Обновлён VIEW: {view}")
        except Exception as e:
            log(f"[ERROR] {view} — {e}")
            errors.append(f"{view} — {e}")

async def check_tables(conn, errors: list):
    expected = [
        "client_info", "client_analytics", "dictionary", "word_category",
        "study_level", "study_levels", "learned_words",
        "client_activity_log", "user_word_stats", "user_progress_by_theme",
        "client_activity_words", "cron_events"
    ]
    for table in expected:
        try:
            count = await conn.fetchval(f"SELECT COUNT(*) FROM {table};")
            log(f"[CHECK] Таблица {table}: {count} записей")
        except Exception as e:
            log(f"[CHECK ERROR] {table}: {e}")
            errors.append(f"{table} — {e}")

async def sync_client_analytics_all():
    log("🔗 Подключение к базе данных...")
    errors = []
    try:
        conn = await asyncpg.connect(**DB)

        # 1. Проверка состояния таблиц
        await check_tables(conn, errors)

        # 2. Обновление VIEW'шек
        await refresh_views(conn, errors)

        # 3. Обновление пользовательского прогресса по темам (через TRUNCATE + INSERT)
        log("[DEBUG] Вызов refresh_user_progress(conn) начинается")
        await refresh_user_progress(conn)
        log("[DEBUG] Вызов refresh_user_progress(conn) завершён — таблица user_progress_by_theme обновлена")

        await conn.close()
        log("✅ Синхронизация завершена")
    except Exception as e:
        log(f"[FATAL ERROR] {e}")


# Точка входа
async def main():
    log("🔥 main() запущен")
    await sync_client_analytics_all()

if __name__ == "__main__":
    asyncio.run(main())
