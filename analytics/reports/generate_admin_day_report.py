import asyncpg
from datetime import date
from core.config import DB
from pathlib import Path

TEMPLATE_PATH = Path(__file__).resolve().parent / "forms" / "admin_day_report.txt"

async def generate_admin_day_report(report_date: date) -> str:
    conn = await asyncpg.connect(**DB)
    try:
        stats = {}

        stats["report_date"] = report_date.strftime("%d.%m.%Y")

        stats["total_users"] = await conn.fetchval(
            "SELECT COUNT(DISTINCT client_id) FROM client_activity_log WHERE date_login = $1",
            report_date
        )

        stats["new_users"] = await conn.fetchval(
            "SELECT COUNT(*) FROM client_info WHERE date_reg = $1",
            report_date
        )

        quiz_row = await conn.fetchrow(
            """
            SELECT COUNT(*) AS quizzes,
                   ROUND(AVG(words_correct_quiz + words_incorrect_quiz), 2) AS avg_words
            FROM client_activity_log
            WHERE date_login = $1
            """, report_date
        )
        stats["quizzes"] = quiz_row["quizzes"] if quiz_row else 0
        stats["avg_words"] = quiz_row["avg_words"] if quiz_row else 0.0

        top_themes = await conn.fetch(
            """
            SELECT wc.cat_name, COUNT(*) AS words_learned
            FROM learned_words lw
            JOIN dictionary d ON d.word_id = lw.word_id
            JOIN word_category wc ON wc.cat_id = d.cat_id
            WHERE lw.learned_at = $1
            GROUP BY wc.cat_name
            ORDER BY words_learned DESC
            LIMIT 3
            """, report_date
        )
        stats["top_themes"] = "\n".join(
            [f" • {r['cat_name']} ({r['words_learned']})" for r in top_themes]
        ) if top_themes else "–"

        top_users = await conn.fetch(
            """
            SELECT ci.username, ca.client_rating
            FROM client_analytics ca
            JOIN client_info ci ON ci.client_id = ca.client_id
            WHERE ca.last_activity_date = $1
            ORDER BY ca.client_rating DESC
            LIMIT 3
            """, report_date
        )
        stats["top_users"] = "\n".join(
            [f" • @{r['username']} ({r['client_rating']})" for r in top_users]
        ) if top_users else "–"

        template = open(TEMPLATE_PATH, encoding="utf-8").read()

        # ⬇️ Быстрый вывод всех показателей для отладки и визуального контроля
        print("📦 Статистика за", report_date.strftime("%Y-%m-%d"))
        for key, value in stats.items():
            print(f"{key}: {value}")

        return template.format(
            report_date=stats["report_date"],
            total_users=stats["total_users"],
            new_users=stats["new_users"],
            quizzes=stats["quizzes"],
            avg_words=f"{stats['avg_words']:.1f}",  # 🔥 округление до 1 знака,
            top_themes=stats["top_themes"],
            top_users=stats["top_users"]
        )

    finally:
        await conn.close()