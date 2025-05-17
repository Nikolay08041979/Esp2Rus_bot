import asyncpg
from core.config import DB, DELETE_INACTIVE_CLIENTS

async def delete_inactive_clients():
    if not DELETE_INACTIVE_CLIENTS:
        print("[CRON] Удаление отключено настройками.")
        return

    conn = await asyncpg.connect(**DB)
    try:
        result = await conn.execute("""
            DELETE FROM client_info
            WHERE client_id NOT IN (
                SELECT DISTINCT client_id FROM client_activity_log
            )
            AND date_reg < CURRENT_DATE - INTERVAL '1 day';
        """)
        print(f"[CRON] Удалены временные клиенты: {result}")
    finally:
        await conn.close()
