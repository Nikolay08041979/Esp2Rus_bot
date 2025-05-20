import asyncpg
from datetime import date
from core.config import DB, flag
from analytics.metrics.calculate_level_current import calculate_level_current
from analytics.personalization.update_user_progress_by_theme import refresh_user_progress
from pathlib import Path

TEMPLATE_PATH = Path(__file__).resolve().parent / "forms" / "user_report.txt"

async def generate_user_report(tg_id: int) -> str:
    conn = await asyncpg.connect(**DB)
    try:
        await refresh_user_progress(conn)

        client = await conn.fetchrow("SELECT * FROM client_info WHERE tg_id = $1", tg_id)
        if client is None:
            return "❌ Для получения отчёта нужно сначала пройти хотя бы одну викторину. Нажмите /start."

        client_id = client["client_id"]
        reg_date = client["date_reg"]
        today = date.today()

        # 🎯 Уровень и группа
        level_id = await calculate_level_current(conn, client_id)
        if level_id:
            row = await conn.fetchrow("""
                SELECT cefr_id_short, lev_id FROM level_matrix WHERE level_id_client = $1
            """, level_id)
            level_display = row["cefr_id_short"] if row else "пока не определен"
            lev_id = row["lev_id"] if row else 1
        else:
            level_display = "пока не определен"
            lev_id = 1

        # 📊 Прогресс по уровню сложности (client_level_progress)
        row = await conn.fetchrow("""
            SELECT coverage_percent FROM client_level_progress
            WHERE client_id = $1 AND lev_id = $2
        """, client_id, lev_id)
        level_progress_percent = round(row["coverage_percent"] or 0, 1) if row else 0.0

        level_changed_days = (today - reg_date).days

        # 🏆 Рейтинг и статистика
        rating_row = await conn.fetchrow("""
            SELECT client_rating FROM client_analytics WHERE client_id = $1
        """, client_id)
        rating = rating_row["client_rating"] if rating_row else 0

        rank_row = await conn.fetchrow("""
            SELECT COUNT(*) + 1 AS rank FROM client_analytics WHERE client_rating > $1
        """, rating)
        rank = rank_row["rank"]

        quiz_row = await conn.fetchrow("""
            SELECT quizzes_finished_total FROM client_analytics WHERE client_id = $1
        """, client_id)
        quiz_count = quiz_row["quizzes_finished_total"]

        words_row = await conn.fetchrow("""
            SELECT COUNT(*) AS total FROM learned_words WHERE client_id = $1
        """, client_id)
        total_words = words_row["total"]

        # 📊 Блок по уровням сложности (client_level_progress)
        level_rows = await conn.fetch("""
            SELECT lev_id, total_words, learned_words, coverage_percent
            FROM client_level_progress
            WHERE client_id = $1
            ORDER BY lev_id
        """, client_id)
        level_names = {1: "начальный", 2: "средний", 3: "продвинутый"}

        level_lines = []
        for row in level_rows:
            if row['learned_words'] > 0:
                lev_id = row['lev_id']
                level_name = level_names.get(lev_id, f"уровень {lev_id}")
                level_lines.append(
                    f"•⁠  ⁠{level_name}: {row['learned_words']}/{row['total_words']} ({row['coverage_percent']}%)"
                )
        level_text = "\n".join(level_lines) if level_lines else "–"


        # 📈 Блок по темам (view_user_progress_by_theme)
        category_rows = await conn.fetch("""
            SELECT cat_name, total_words, learned_words, percent_done
            FROM view_user_progress_by_theme
            WHERE client_id = $1
            ORDER BY cat_name
        """, client_id)
        category_lines = [
            f"•⁠  ⁠{row['cat_name']}: {row['learned_words']}/{row['total_words']} ({row['percent_done']}%)"
            for row in category_rows if row['learned_words'] > 0
        ]
        category_text = "\n".join(category_lines) if category_lines else "–"

        # 📤 Итоговая подстановка в шаблон
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