
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
from analytics.metrics.calculate_level_current import calculate_level_current
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



async def save_client_analytics(client_id: int) -> float:
    try:
        conn = await asyncpg.connect(**DB)

        # 📊 1. Основные метрики
        row = await conn.fetchrow("""
            SELECT COUNT(*) AS total, AVG(score_quiz) AS avg_score
            FROM client_activity_log
            WHERE client_id = $1
        """, client_id)
        total_quizzes = row["total"]
        avg_score = row["avg_score"]

        client_rating = await get_client_rating(conn, client_id)

        # 🧠 2. Расчёт уровня владения (CEFR)
        level_id_current = await calculate_level_current(conn, client_id)

        # 💾 Обновление client_analytics
        await conn.execute("""
                    INSERT INTO client_analytics (
                        client_id, last_activity_date,
                        quizzes_finished_total, quizzes_score_total,
                        client_rating, level_id_current, date_level_upgraded
                    ) VALUES (
                        $1, CURRENT_DATE,
                        $2, $3,
                        $4, $5, CURRENT_DATE
                    )
                    ON CONFLICT (client_id) DO UPDATE SET
                        last_activity_date = CURRENT_DATE,
                        quizzes_finished_total = EXCLUDED.quizzes_finished_total,
                        quizzes_score_total = EXCLUDED.quizzes_score_total,
                        client_rating = EXCLUDED.client_rating,
                        level_id_current = EXCLUDED.level_id_current,
                        date_level_upgraded = CASE
                            WHEN client_analytics.level_id_current IS DISTINCT FROM EXCLUDED.level_id_current
                            THEN CURRENT_DATE
                            ELSE client_analytics.date_level_upgraded
                        END
                """, client_id, total_quizzes, round(avg_score or 0, 2), client_rating, level_id_current)

        print(f"[AGG] Обновлены агрегаты клиента {client_id}: total={total_quizzes}, avg={avg_score}, rating={client_rating}, level={level_id_current}")
        return client_rating

    except Exception as e:
        print(f"[AGG ERROR] Ошибка при обновлении client_analytics для client_id={client_id}: {e}")
        return None

    finally:
        await conn.close()
