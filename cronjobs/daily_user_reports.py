# 📤 daily_user_reports.py — Только отправка admin-дневного отчёта

import asyncio
import asyncpg
from datetime import datetime, date, timedelta
from core.config import DB, ENABLE_AUTO_REPORTS, ADMIN_IDS

from analytics.reports.generate_admin_day_report import generate_admin_day_report
from bot.utils.telegram import send_report_to_admin


async def log_cron_event(conn, task_name, status, details=""):
    await conn.execute(
        """
        INSERT INTO cron_events (task_name, status, timestamp, details)
        VALUES ($1, $2, $3, $4)
        """,
        task_name, status, datetime.now(), details
    )

async def main():
    if not ENABLE_AUTO_REPORTS:
        print("[CRON] Автоотчёты отключены флагом ENABLE_AUTO_REPORTS")
        return

    conn = await asyncpg.connect(**DB)
    try:
        report_date = date.today() - timedelta(days=1)
        report_text = await generate_admin_day_report(report_date)

        for admin_id in ADMIN_IDS:
            try:
                await send_report_to_admin(admin_id, report_text)
            except Exception as e:
                print(f"[ERROR] Не удалось отправить отчёт администратору {admin_id}: {e}")

        await log_cron_event(conn, "admin_day_report", "success", f"Sent to {len(ADMIN_IDS)} admins for {report_date}")

    except Exception as e:
        await log_cron_event(conn, "admin_day_report", "failed", str(e))
        print(f"[CRON ERROR] {e}")
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())