# 📄 db/create/create_cron_events.py

import asyncpg
from core.config import DB

CREATE_SQL = """
CREATE TABLE IF NOT EXISTS cron_events (
    id SERIAL PRIMARY KEY,
    task_name TEXT NOT NULL,
    status TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details TEXT
);
"""

async def create_cron_events_table():
    try:
        conn = await asyncpg.connect(**DB)
        await conn.execute(CREATE_SQL)
        await conn.close()
        print("[OK] Таблица cron_events создана (если её не было).")
    except Exception as e:
        print(f"[ERROR] Ошибка при создании cron_events: {e}")
