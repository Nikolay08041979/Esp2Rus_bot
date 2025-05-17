import asyncio
import asyncpg
import subprocess
import argparse
from datetime import datetime
from pathlib import Path
from core.config import DB, ENABLE_DROP_TABLES, ENABLE_RESTORE_DATA, BASE_DIR, LOGS_DIR
from db.install_config import INSTALL_SCHEMA
from core.config import ADMIN_IDS, BOT_TOKEN
from aiogram import Bot

# === Пути ===
CREATE_DIR = BASE_DIR / "db" / "create" / "tables"
VIEW_DIR = BASE_DIR / "db" / "create" / "views"
DUMP_FILE = BASE_DIR / "backup_7_tables.sql"
ANALYTICS_SCRIPT = BASE_DIR / "analytics" / "metrics" / "run_sync_all_clients_with_tg_notify.py"
LOG_FILE = LOGS_DIR / "run_install.log"

# === Таблицы из дампа
RESTORED_TABLES = {
    "client_info", "client_analytics", "dictionary", "word_category",
    "study_level", "study_levels", "learned_words"
}

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

async def execute_sql_file(conn, file_path, object_type="SQL", errors=None):
    try:
        sql = file_path.read_text()
        await conn.execute(sql)
        log(f"[OK] {object_type}: {file_path.name}")
    except Exception as e:
        log(f"[ERROR] {object_type}: {file_path.name} — {e}")
        if errors is not None:
            errors.append(f"{object_type}: {file_path.name} — {e}")

async def drop_restored_tables(conn, errors):
    for table in RESTORED_TABLES:
        try:
            await conn.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE;')
            log(f"🗑 Удалена таблица (из дампа): {table}")
        except Exception as e:
            log(f"[DROP ERROR] {table}: {e}")
            errors.append(f"DROP {table} — {e}")

async def install_tables(conn, errors):
    log("🔁 Пересоздание таблиц...")
    for table in sorted(INSTALL_SCHEMA.get("tables", {}), key=lambda k: INSTALL_SCHEMA["tables"][k]):
        if table in RESTORED_TABLES:
            continue
        if ENABLE_DROP_TABLES:
            try:
                await conn.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE;')
                log(f"🗑 Удалена таблица: {table}")
            except Exception as e:
                log(f"[DROP ERROR] {table}: {e}")
                errors.append(f"DROP {table} — {e}")
        file_path = CREATE_DIR / f"{table}.sql"
        if file_path.exists():
            await execute_sql_file(conn, file_path, "TABLE", errors)
        else:
            log(f"[SKIP] Файл {file_path.name} не найден")
            errors.append(f"Файл отсутствует: {file_path.name}")

async def install_views(conn, errors):
    log("🔁 Пересоздание VIEW'шек...")
    for view in sorted(INSTALL_SCHEMA.get("views", {}), key=lambda k: INSTALL_SCHEMA["views"][k]):
        file_path = VIEW_DIR / f"{view}.sql"
        if file_path.exists():
            await execute_sql_file(conn, file_path, "VIEW", errors)
        else:
            log(f"[SKIP] Файл {file_path.name} не найден")
            errors.append(f"Файл отсутствует: {file_path.name}")

async def restore_from_dump(errors):
    if not DUMP_FILE.exists():
        log(f"[SKIP] Дамп {DUMP_FILE} не найден.")
        errors.append(f"Дамп отсутствует: {DUMP_FILE}")
        return
    log(f"♻️ Восстановление из дампа: {DUMP_FILE.name}")
    cmd = [
        "psql",
        "-U", DB["user"],
        "-h", DB["host"],
        "-p", str(DB["port"]),
        "-d", DB["database"],
        "-f", str(DUMP_FILE)
    ]
    try:
        subprocess.run(cmd, check=True)
        log("✅ Восстановление завершено")
    except subprocess.CalledProcessError as e:
        log(f"[RESTORE ERROR] {e}")
        errors.append(f"Ошибка восстановления из дампа: {e}")

async def run_post_restore_checks(conn, errors):
    log("🔍 Пост-проверка: валидация client_id в client_analytics ...")
    try:
        result = await conn.fetchval("""
            SELECT COUNT(*) FROM client_analytics
            WHERE client_id NOT IN (SELECT client_id FROM client_info);
        """)
        if result == 0:
            log("✅ Все client_id в client_analytics соответствуют client_info")
        else:
            log(f"⚠️ Найдено {result} записей client_analytics без client_info")

        log("🔍 Проверка заполненности level_id_current...")
        null_levels = await conn.fetchval("""
            SELECT COUNT(*) FROM client_analytics
            WHERE level_id_current IS NULL;
        """)
        if null_levels == 0:
            log("✅ Все записи в client_analytics содержат level_id_current")
        else:
            log(f"⚠️ Найдено {null_levels} записей без уровня level_id_current")

    except Exception as e:
        log(f"[POST-CHECK ERROR] {e}")
        errors.append(f"POST-CHECK ERROR: {e}")

async def notify_admins(message: str):
    try:
        bot = Bot(token=BOT_TOKEN)
        for admin_id in ADMIN_IDS:
            await bot.send_message(chat_id=admin_id, text=message)
        await bot.session.close()
    except Exception as e:
        log(f"[TELEGRAM ERROR] Ошибка отправки уведомления: {e}")

async def run_install():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sync", action="store_true", help="Запускать sync метрику после установки")
    args = parser.parse_args()

    errors = []
    conn = await asyncpg.connect(**DB)
    log(f"🔗 Подключение к базе данных {DB['database']}")

    if ENABLE_RESTORE_DATA:
        await drop_restored_tables(conn, errors)
        await restore_from_dump(errors)

    await install_tables(conn, errors)
    await install_views(conn, errors)
    await run_post_restore_checks(conn, errors)
    await conn.close()

    if args.sync:
        log("🚀 Запуск sync метрики...")
        try:
            print("[DEBAG]🔧 Запуск обновления метрик...")
            subprocess.run(["python", "-m", "analytics.metrics.run_sync_all_clients_with_tg_notify"], check=True)
            log("✅ Метрики успешно обновлена")
        except subprocess.CalledProcessError as e:
            errors.append(f"Ошибка запуска метрик: {e}")

    # Финальный результат
    if not errors:
        summary = "🧾 РЕЗУЛЬТАТ УСТАНОВКИ:\n✅ Установка завершена без ошибок."
    else:
        summary = "🧾 РЕЗУЛЬТАТ УСТАНОВКИ:\n⚠️ Установка завершена с ошибками:\n" + "\n".join([f"  - {e}" for e in errors])

    for line in summary.split("\n"):
        log(line)

    try:
        await notify_admins(summary)
    except Exception:
        pass

if __name__ == "__main__":
    asyncio.run(run_install())
