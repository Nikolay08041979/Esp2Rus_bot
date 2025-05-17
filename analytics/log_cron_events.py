# 📄 analytics/log_cron_event.py

import asyncpg
from core.config import DB
from datetime import datetime

async def log_cron_event(task_name: str, status: str, details: str = ""):
    try:
        conn = await asyncpg.connect(**DB)
        await conn.execute(
            """
            INSERT INTO cron_events (task_name, status, timestamp, details)
            VALUES ($1, $2, $3, $4)
            """,
            task_name, status, datetime.now(), details
        )
        await conn.close()
    except Exception as e:
        print(f"[CRON_LOG ERROR] Не удалось записать событие: {e}")
