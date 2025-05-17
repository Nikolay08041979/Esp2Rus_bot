# analytics/reports/generate_cron_log_report.py

import asyncpg
import csv
import io
from datetime import date, timedelta
from core.config import DB

MAX_DAYS = 30  # максимум глубины отчёта

async def generate_cron_log_report(days: int = 30) -> str:
    # ⛔ Ограничиваем глубину отчёта
    days = min(days, MAX_DAYS)
    since_date = date.today() - timedelta(days=days - 1)

    conn = await asyncpg.connect(**DB)
    try:
        rows = await conn.fetch(
            """
            SELECT id, task_name, status, timestamp::date AS log_date, timestamp::time AS log_time, details
            FROM cron_events
            WHERE timestamp >= $1
            ORDER BY timestamp DESC
            """,
            since_date
        )

        if not rows:
            return "❌ Логов за последние {days} дней не найдено. Возможно, данных меньше — отчёт покажет всё, что есть."

        # 📄 Генерация CSV в память
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "task_name", "status", "date", "time", "details"])

        for row in rows:
            writer.writerow([
                row["id"],
                row["task_name"],
                row["status"],
                row["log_date"].strftime("%Y-%m-%d"),
                row["log_time"].strftime("%H:%M:%S"),
                row["details"]
            ])

        return output.getvalue()

    finally:
        await conn.close()
