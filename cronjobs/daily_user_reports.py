# 📤 daily_user_reports.py — Ежедневная отправка отчётов пользователям и администраторам

import asyncio
import asyncpg
from datetime import datetime, date
from core.config import DB, ENABLE_AUTO_REPORTS, ADMIN_IDS
from analytics.reports.user_report import generate_user_report
from analytics.reports.admin_report import generate_admin_day_report
from bot.utils.telegram import send_report_to_user, send_report_to_admin  # предположим, есть такие утилиты

async def get_all_active_clients(conn):
    rows = await conn.fetch(
        """
        SELECT DISTINCT client_id, tg_id
        FROM client_info
        WHERE tg_id IS NOT NULL
        AND client_id IN (
            SELECT DISTINCT client_id
            FROM client_activity_log
            WHERE date_login >= CURRENT_DATE - INTERVAL '2 days'
        )
        """
    )
    return rows

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
        active_clients = await get_all_active_clients(conn)
        total_sent = 0

        for client in active_clients:
            try:
                tg_id = client["tg_id"]
                report_text = await generate_user_report(tg_id)
                await send_report_to_user(tg_id, report_text)
                total_sent += 1
            except Exception as e:
                print(f"[ERROR] Не удалось отправить отчёт пользователю {tg_id}: {e}")

        # Отправка админского отчёта
        try:
            admin_report_text, admin_csv = await generate_admin_day_report(date.today())
            for admin_id in ADMIN_IDS:
                await send_report_to_admin(admin_id, admin_report_text, admin_csv)
        except Exception as e:
            print(f"[ERROR] Ошибка при отправке отчёта администраторам: {e}")

        await log_cron_event(conn, "daily_user_reports", "success", f"Users: {total_sent}, Admins: {len(ADMIN_IDS)}")

    except Exception as e:
        await log_cron_event(conn, "daily_user_reports", "failed", str(e))
        print(f"[CRON ERROR] {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(main())