import asyncio
import asyncpg
import os
from pathlib import Path
from core.config import DB
from db.install_config import INSTALL_SCHEMA

# Настройки
ENABLE_DROP = True
ENABLE_RESTORE = True

CREATE_DIR = Path(__file__).resolve().parent / "create"
BACKUP_DIR = Path(__file__).resolve().parent.parent / "data" / "backup" / "sql"

async def execute_sql_file(conn, file_path, errors: list):
    try:
        sql = file_path.read_text()
        await conn.execute(sql)
        print(f"[OK] Выполнен: {file_path.name}")
    except Exception as e:
        print(f"[ERROR] Ошибка в {file_path.name}: {e}")
        errors.append(f"❌ {file_path.name} — {e}")

async def restore_data(conn, table_name, errors: list):
    backup_file = BACKUP_DIR / f"{table_name}_latest.sql"
    if backup_file.exists():
        print(f"♻️ Восстановление данных из {backup_file.name}")
        try:
            sql = backup_file.read_text()
            await conn.execute(sql)
            print(f"[RESTORED] {table_name}")
        except Exception as e:
            print(f"[RESTORE ERROR] {table_name}: {e}")
            errors.append(f"⚠️ Восстановление {table_name} — {e}")
    else:
        print(f"[SKIP] Нет файла восстановления для {table_name}")

async def install():
    conn = await asyncpg.connect(**DB)
    print("🔗 Подключено к базе данных")

    errors = []

    # Установка таблиц
    for table in sorted(INSTALL_SCHEMA.get("tables", {}), key=lambda k: INSTALL_SCHEMA["tables"][k]):
        if ENABLE_DROP:
            try:
                await conn.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
                print(f"🗑 Удалена таблица: {table}")
            except Exception as e:
                print(f"[DROP ERROR] {table}: {e}")
                errors.append(f"❌ DROP {table} — {e}")

        file_path = CREATE_DIR / f"create_table_{table}.sql"
        if file_path.exists():
            print(f"⚙️ Создание таблицы: {table}")
            await execute_sql_file(conn, file_path, errors)

            if ENABLE_RESTORE:
                await restore_data(conn, table, errors)
        else:
            print(f"[SKIP] Файл не найден: {file_path.name}")
            errors.append(f"📂 create_table_{table}.sql не найден")

    # Установка VIEW
    for view in sorted(INSTALL_SCHEMA.get("views", {}), key=lambda k: INSTALL_SCHEMA["views"][k]):
        file_path = CREATE_DIR / f"create_view_{view}.sql"
        if file_path.exists():
            print(f"🔍 Создание VIEW: {view}")
            await execute_sql_file(conn, file_path, errors)
        else:
            print(f"[SKIP] Файл не найден: {file_path.name}")
            errors.append(f"📂 create_view_{view}.sql не найден")

    await conn.close()

    # Финальный статус
    print("\n🧾 РЕЗУЛЬТАТ УСТАНОВКИ:")
    if not errors:
        print("✅ Установка завершена без ошибок.")
    else:
        print("⚠️ Установка завершена с ошибками:")
        for err in errors:
            print(f"   - {err}")

if __name__ == "__main__":
    asyncio.run(install())
