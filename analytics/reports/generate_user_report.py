from analytics.reports.user_report import generate_user_report as generate_user_report_text
import asyncpg
from core.config import DB

async def generate_user_report(user_ref: str | int) -> str:
    conn = await asyncpg.connect(**DB)
    try:
        if isinstance(user_ref, str) and user_ref.startswith("@"):
            tg_id = await conn.fetchval("SELECT tg_id FROM client_info WHERE username = $1", user_ref[1:])
        else:
            tg_id = int(user_ref)
    finally:
        await conn.close()

    return await generate_user_report_text(tg_id)
