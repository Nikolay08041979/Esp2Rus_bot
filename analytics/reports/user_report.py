import asyncpg
from datetime import date
from core.config import DB, flag

TEMPLATE_PATH = "analytics/reports/forms/[template]user_report.txt"

async def generate_user_report(tg_id: int) -> str:
    conn = await asyncpg.connect(**DB)
    try:
        client = await conn.fetchrow("SELECT * FROM client_info WHERE tg_id = $1", tg_id)
        analytics = await conn.fetchrow("SELECT * FROM client_analytics WHERE client_id = $1", client["client_id"])
        reg_date = client["date_reg"]
        today = date.today()

        rating = analytics["client_rating"]
        rank_row = await conn.fetchrow("SELECT COUNT(*) + 1 AS rank FROM client_analytics WHERE client_rating > $1", rating)
        rank = rank_row["rank"]

        level_id = analytics["level_id_current"]
        quiz_row = await conn.fetchrow("SELECT COUNT(*) AS total FROM client_activity_log WHERE client_id = $1", client["client_id"])
        quiz_count = quiz_row["total"]

        words_row = await conn.fetchrow("SELECT COUNT(*) AS total FROM learned_words WHERE client_id = $1", client["client_id"])
        total_words = words_row["total"]

        level_row = await conn.fetchrow("SELECT level_client FROM study_levels WHERE level_id = $1", level_id) if level_id else None
        if level_id and level_row and level_row["level_client"]:
            level_raw = level_row["level_client"]
            level_display = level_raw.split("–")[0].strip().upper() + " — " + level_raw.strip()
        else:
            level_display = "пока не определен\n🛈 Для определения уровня необходимо выучить хотя бы 50% слов одного уровня сложности"

        if level_id:
            coverage_row = await conn.fetchrow(
                "SELECT coverage_percent FROM client_level_progress WHERE client_id = $1 AND lev_id = $2",
                client["client_id"], level_id
            )
            level_progress_percent = int(coverage_row["coverage_percent"]) if coverage_row and coverage_row["coverage_percent"] else 0
        else:
            max_row = await conn.fetchrow(
                "SELECT MAX(coverage_percent) AS max_percent FROM client_level_progress WHERE client_id = $1",
                client["client_id"]
            )
            level_progress_percent = int(max_row["max_percent"]) if max_row and max_row["max_percent"] is not None else 0

        level_updated_at = analytics.get("level_updated_at")
        level_changed_days = (today - (level_updated_at or reg_date)).days

        # 📈 Прогресс по категориям (агрегировано)
        category_rows = await conn.fetch(
            """
            SELECT wc.cat_name, 
                   SUM(upt.learned_words) AS learned, 
                   SUM(upt.total_words) AS total
            FROM user_progress_by_theme upt
            JOIN word_category wc ON wc.cat_id = upt.cat_id
            WHERE upt.client_id = $1
            GROUP BY wc.cat_name
            HAVING SUM(upt.learned_words) > 0
            ORDER BY learned DESC
            """, client["client_id"]
        )
        category_lines = [
            f"•⁠  ⁠{row['cat_name']}: {row['learned']}/{row['total']} ({int(100 * row['learned'] / row['total'])}%)"
            for row in category_rows
        ]
        category_text = "\n".join(category_lines) if category_lines else "–"

        # 📊 Прогресс по уровням
        level_rows = await conn.fetch(
            """
            SELECT s.lev_name, SUM(upt.learned_words) AS learned, SUM(upt.total_words) AS total
            FROM user_progress_by_theme upt
            JOIN study_level s ON s.lev_id = upt.level_id
            WHERE upt.client_id = $1
            GROUP BY s.lev_name, s.lev_id
            HAVING SUM(upt.learned_words) > 0
            ORDER BY s.lev_id
            """, client["client_id"]
        )
        level_lines = [
            f"•⁠  ⁠{row['lev_name']}: {row['learned']}/{row['total']} ({int(100 * row['learned'] / row['total'])}%)"
            for row in level_rows
        ]
        level_text = "\n".join(level_lines) if level_lines else "–"

        # Загрузка шаблона и форматирование
        with open(TEMPLATE_PATH, encoding="utf-8") as f:
            template = f.read()

        return template.format(
            first_name=client["first_name"],
            username=client["username"] or "user",
            tg_id=tg_id,
            reg_date=reg_date.strftime('%-d %B %Y'),
            days_with_us=(today - reg_date).days,
            rating=rating,
            rank=rank,
            level_display=level_display,
            level_progress_percent=level_progress_percent,
            level_changed_days=level_changed_days,
            total_words=total_words,
            quiz_count=quiz_count,
            level_block=level_text,
            category_block=category_text,
            flag=flag
        )
    finally:
        await conn.close()