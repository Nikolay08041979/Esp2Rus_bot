
# 📂 analytics_v2.py

"""
Orchestration Layer:
- Централизует вызовы save_client_activity_log и save_client_analytics
- Содержит всю отладочную, логирующую и тестовую инфраструктуру
- Является основной точкой входа на этапе staging и продакшна
"""

import asyncpg
from core.config import DB
import asyncio
from datetime import datetime
import logging
import json
import os

from core.config import USE_ANALYTICS_V2

from analytics.save_client_activity_log import save_activity
from analytics.save_client_analytics import save_client_analytics

logging.basicConfig(level=logging.DEBUG)

async def log_client_activity(time_start, time_finish, data: dict):
    logging.debug("🧩 Оркестратор запущен")
    logging.debug("Содержимое data: %s", json.dumps(data, indent=4, default=str))

    if not USE_ANALYTICS_V2:
        logging.warning("⚠️ Аналитический стек V2 отключён. Выход.")
        return

    try:
        await save_activity(data)

        client_id = await extract_client_id(data["tg_id"])
        client_rating = await save_client_analytics(client_id)

        # ✅ лог в файл
        log_dir = "data/logs/analytics_debug"
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "quiz_weight_v2.log")
        with open(log_path, "a") as f:
            f.write(f"{datetime.now()}: client_id={client_id}, quiz_weight={data.get('quiz_weight')}, client_rating={client_rating}\n")

        # ✅ лог в cron_events
        await log_cron_event("save_client_analytics", "success", f"client_id={client_id}, rating={client_rating}")

        logging.info(f"[OK] Данные по клиенту {client_id} обработаны и записаны.")

    except Exception as e:
        await log_cron_event("save_client_analytics", "failed", str(e))
        logging.error(f"[❌ ERROR] Ошибка в orchestration: {e}")


async def extract_client_id(tg_id: int) -> int:
    conn = await asyncpg.connect(**DB)
    row = await conn.fetchrow("SELECT client_id FROM client_info WHERE tg_id = $1", tg_id)
    await conn.close()
    return row["client_id"] if row else -1

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
