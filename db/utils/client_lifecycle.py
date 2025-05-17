import asyncpg
from core.config import DB

async def ensure_client_registered(tg_user) -> None:
    """Добавляет клиента в client_info, если его ещё нет."""
    conn = await asyncpg.connect(**DB)
    try:
        result = await conn.fetchrow("SELECT client_id FROM client_info WHERE tg_id = $1", tg_user.id)
        if not result:
            await conn.execute("""
                INSERT INTO client_info (tg_id, username, first_name, last_name, date_reg, language_code)
                VALUES ($1, $2, $3, $4, CURRENT_DATE, $5)
            """, tg_user.id, tg_user.username, tg_user.first_name, tg_user.last_name, tg_user.language_code)
            print(f"[START] Зарегистрирован новый клиент: {tg_user.id}")
    finally:
        await conn.close()