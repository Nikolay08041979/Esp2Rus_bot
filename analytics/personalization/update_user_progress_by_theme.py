import asyncpg
from core.config import DB

async def update_user_progress_by_theme(conn: asyncpg.Connection, client_id: int):
    await conn.execute("""
        DELETE FROM user_progress_by_theme WHERE client_id = $1;
    """, client_id)

    await conn.execute("""
        INSERT INTO user_progress_by_theme (
            client_id, cat_id, level_id, total_words, learned_words, percent_done
        )
        SELECT
            $1 AS client_id,
            d.cat_id,
            d.lev_id,
            COUNT(*) AS total_words,
            COUNT(lw.word_id) AS learned_words,
            ROUND(COUNT(lw.word_id) * 1.0 / COUNT(*)::numeric, 2) AS percent_done
        FROM dictionary d
        LEFT JOIN learned_words lw ON lw.word_id = d.word_id AND lw.client_id = $1
        GROUP BY d.cat_id, d.lev_id;
    """, client_id)