import asyncpg

async def refresh_user_progress(conn: asyncpg.Connection):
    print("🟢 refresh_user_progress() вызван")
    try:
        async with conn.transaction():
            await conn.execute("TRUNCATE TABLE user_progress_by_theme")
            print("🧹 user_progress_by_theme очищена")

            result = await conn.execute("""
                INSERT INTO user_progress_by_theme (
                    client_id, cat_id, total_words, learned_words, percent_done, updated_at
                )
                SELECT
                    ci.client_id,
                    d.cat_id,
                    COUNT(*) AS total_words,
                    COUNT(lw.word_id) AS learned_words,
                    ROUND(COUNT(lw.word_id) * 100.0 / COUNT(*)::numeric, 2) AS percent_done,
                    CURRENT_DATE
                FROM dictionary d
                CROSS JOIN client_info ci
                LEFT JOIN learned_words lw ON lw.word_id = d.word_id AND lw.client_id = ci.client_id
                WHERE d.cat_id IS NOT NULL
                GROUP BY ci.client_id, d.cat_id
            """)
            print(f"🟢 Обновлён прогресс по категориям: {result}")

    except Exception as e:
        print(f"❌ Ошибка при обновлении user_progress_by_theme: {e}")