import asyncpg
import csv
from datetime import date, timedelta
from core.config import DB

async def generate_admin_report_csv(days: int = 30) -> str:
    conn = await asyncpg.connect(**DB)
    try:
        today = date.today()
        start_date = today - timedelta(days=days - 1)
        from_str = start_date.strftime("%d.%m.%Y")
        to_str = today.strftime("%d.%m.%Y")
        output_path = f"admin_report_{from_str}_{to_str}.csv"

        report_data = []

        for i in range(days):
            report_date = start_date + timedelta(days=i)
            row = {"date": report_date.strftime("%Y-%m-%d")}

            row["total_users"] = await conn.fetchval(
                "SELECT COUNT(DISTINCT client_id) FROM client_activity_log WHERE date_login = $1",
                report_date
            )

            row["new_users"] = await conn.fetchval(
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
            row["quizzes"] = quiz_row["quizzes"] if quiz_row else 0
            row["avg_words"] = quiz_row["avg_words"] if quiz_row else 0.0

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
            row["top_themes"] = "; ".join([f"{r['cat_name']} ({r['words_learned']})" for r in top_themes]) if top_themes else "-"

            top_users = await conn.fetch(
                """
                SELECT ci.username, ca.client_rating
                FROM client_analytics ca
                JOIN client_info ci ON ci.client_id = ca.client_id
                WHERE ca.last_active = $1
                ORDER BY ca.client_rating DESC
                LIMIT 3
                """, report_date
            )
            row["top_users"] = "; ".join([f"@{r['username']} ({r['client_rating']})" for r in top_users]) if top_users else "-"

            report_data.append(row)

        fieldnames = ["date", "total_users", "new_users", "quizzes", "avg_words", "top_themes", "top_users"]
        with open(output_path, "w", encoding="utf-8", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(report_data)

        return output_path

    finally:
        await conn.close()