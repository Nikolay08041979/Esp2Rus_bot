# analytics/personalization/update_learned_words.py

import asyncpg
from loguru import logger


async def update_learned_words(conn: asyncpg.Connection, client_id: int) -> None:
    """
    Обновляет таблицу learned_words: добавляет слова, на которые пользователь дал 3 и более
    правильных ответов независимо от времени и квизов.
    """
    logger.info(f"🔁 Обновление выученных слов для client_id={client_id}")
    await conn.execute("""
        INSERT INTO learned_words (client_id, word_id)
        SELECT client_id, word_id
        FROM (
            SELECT cal.client_id, caw.word_id,
                   COUNT(*) FILTER (WHERE caw.is_correct = TRUE) AS correct_count
            FROM client_activity_words caw
            JOIN client_activity_log cal ON cal.id = caw.activity_id
            WHERE cal.client_id = $1
            GROUP BY cal.client_id, caw.word_id
        ) sub
        WHERE correct_count >= 3
        ON CONFLICT DO NOTHING;
    """, client_id)
    logger.success(f"✅ Выученные слова обновлены для client_id={client_id}")
