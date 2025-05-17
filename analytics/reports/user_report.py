import asyncpg
from datetime import date
from core.config import DB, flag
from analytics.metrics.calculate_level_current import calculate_level_current
from pathlib import Path

TEMPLATE_PATH = Path(__file__).resolve().parent / "forms" / "user_report.txt"

async def generate_user_report(tg_id: int) -> str:
    conn = await asyncpg.connect(**DB)
    try:
        client = await conn.fetchrow("SELECT * FROM client_info WHERE tg_id = $1", tg_id)
        if client is None:
            return "❌ Для получения отчёта нужно сначала пройти хотя бы одну викторину. Нажмите /start."

        client_id = client["client_id"]
        reg_date = client["date_reg"]
        today = date.today()

        # 🎯 Уровень пересчитываем онлайн через внешнюю функцию
        level_id = await calculate_level_current(conn, client_id)

        rating_row = await conn.fetchrow("SELECT client_rating FROM client_analytics WHERE client_id = $1", client_id)
        rating = rating_row["client_rating"] if rating_row else 0

        rank_row = await conn.fetchrow("SELECT COUNT(*) + 1 AS rank FROM client_analytics WHERE client_rating > $1", rating)
        rank = rank_row["rank"]

        quiz_row = await conn.fetchrow("SELECT quizzes_finished_total FROM client_analytics WHERE client_id = $1", client_id)
        quiz_count = (quiz_row["quizzes_finished_total"])


        words_row = await conn.fetchrow("SELECT COUNT(*) AS total FROM learned_words WHERE client_id = $1", client_id)
        total_words = words_row["total"]

        # 📌 Получаем CEFR-метку и прогресс по уровню
        if level_id:
            row = await conn.fetchrow(
                "SELECT cefr_id_short, lev_id FROM level_matrix WHERE level_id_client = $1",
                level_id
            )
            if row:
                level_display = row["cefr_id_short"]
                lev_id = row["lev_id"]
            else:
                level_display = "пока не определен"
                lev_id = 1
        else:
            level_display = "пока не определен"
            lev_id = 1  # fallback на начальный уровень для отображения прогресса

        # ✅ Вычисляем прогресс по выбранному уровню (даже если уровень не присвоен)
        row = await conn.fetchrow(
            """
            SELECT COUNT(*) FILTER (WHERE lw.word_id IS NOT NULL) * 100.0 / NULLIF(COUNT(*), 0) AS progress
            FROM dictionary d
            LEFT JOIN learned_words lw ON lw.word_id = d.word_id AND lw.client_id = $1
            WHERE d.lev_id = $2
            """, client_id, lev_id
        )
        level_progress_percent = round(row["progress"] or 0, 1)

        # 🕒 Дата изменения уровня (пока = дата регистрации)
        level_updated_at = reg_date
        level_changed_days = (today - level_updated_at).days

        # 📈 Прогресс по категориям
        category_rows = await conn.fetch(
            """
            SELECT cat_name, 
                   SUM(learned_words) AS learned, 
                   SUM(total_words) AS total
            FROM view_user_progress_by_theme
            WHERE client_id = $1
            GROUP BY cat_name
            HAVING SUM(learned_words) > 0
            ORDER BY learned DESC
            """, client_id
        )

        category_lines = [
            f"•⁠  ⁠{row['cat_name']}: {row['learned']}/{row['total']} ({int(100 * row['learned'] / row['total'])}%)"
            for row in category_rows
        ]
        category_text = "\n".join(category_lines) if category_lines else "–"

        # 📊 Прогресс по уровням сложности (по client_level_progress)
        level_rows = await conn.fetch(
            """
            SELECT
                s.lev_name,
                d.lev_id,
                COUNT(*) AS total_words,
                COUNT(lw.word_id) AS learned_words
            FROM dictionary d
            JOIN study_level s ON s.lev_id = d.lev_id
            LEFT JOIN learned_words lw ON lw.word_id = d.word_id AND lw.client_id = $1
            GROUP BY s.lev_name, d.lev_id
            ORDER BY d.lev_id
            """, client_id
        )

        level_lines = []
        for row in level_rows:
            total = row["total_words"]
            learned = row["learned_words"]
            percent = round(learned * 100.0 / total, 1) if total > 0 else 0.0
            if learned > 0:
                level_lines.append(f"•⁠  ⁠{row['lev_name']}: {learned}/{total} ({percent}%)")

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
            level_progress_percent=level_progress_percent,  # если будет — можно подтягивать отдельно
            level_changed_days=level_changed_days,
            total_words=total_words,
            quiz_count=quiz_count,
            level_block=level_text,
            category_block=category_text,
            flag=flag
        )
    finally:
        await conn.close()