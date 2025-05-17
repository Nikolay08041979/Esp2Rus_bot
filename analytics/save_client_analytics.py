
# 📄 save_client_analytics.py

"""
Модуль агрегирования клиентской статистики:
- quizzes_finished_total
- quizzes_score_total
- client_rating
- (в будущем) level_id_current

Вызывается после логирования client_activity_log.
"""

import asyncpg
from datetime import datetime
from core.config import DB
from analytics.metrics.calculate_client_rating import get_client_rating
# from analytics.metrics.update_level_current_with_matrix import update_level_current  # будущий импорт

async def save_client_analytics(client_id: int):
    try:
        conn = await asyncpg.connect(**DB)

        # Получаем агрегаты из истории
        row = await conn.fetchrow("""
            SELECT COUNT(*) AS total, AVG(score_quiz) AS avg_score
            FROM client_activity_log
            WHERE client_id = $1
        """, client_id)
        total_quizzes = row["total"]
        avg_score = row["avg_score"]

        client_rating = await get_client_rating(conn, client_id)

        await conn.execute("""
            INSERT INTO client_analytics (
                client_id, last_login_date, quizzes_finished_total, quizzes_score_total, client_rating
            ) VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (client_id) DO UPDATE SET
                last_login_date = EXCLUDED.last_login_date,
                quizzes_finished_total = EXCLUDED.quizzes_finished_total,
                quizzes_score_total = EXCLUDED.quizzes_score_total,
                client_rating = EXCLUDED.client_rating
        """, client_id, datetime.now().date(), total_quizzes, round(avg_score, 2), client_rating)

        print(f"[AGG] Обновлены агрегаты клиента {client_id}: total={total_quizzes}, avg={avg_score}, rating={client_rating}")

        # TODO: в будущем — обновить level_id_current
        # await update_level_current(conn, client_id)

    except Exception as e:
        print(f"[AGG ERROR] Ошибка при обновлении client_analytics для client_id={client_id}: {e}")

    finally:
        await conn.close()
