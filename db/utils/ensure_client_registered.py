async def ensure_client_registered(message: Message):
    conn = await asyncpg.connect(**DB)
    try:
        result = await conn.fetchrow("SELECT client_id FROM client_info WHERE tg_id = $1", message.from_user.id)
        if not result:
            await conn.execute("""
                INSERT INTO client_info (tg_id, username, first_name, last_name, date_reg, language_code)
                VALUES ($1, $2, $3, $4, CURRENT_DATE, $5)
            """, message.from_user.id, message.from_user.username, message.from_user.first_name,
                 message.from_user.last_name, message.from_user.language_code)
            print(f"[START] Зарегистрирован новый клиент: {message.from_user.id}")
    finally:
        await conn.close()
