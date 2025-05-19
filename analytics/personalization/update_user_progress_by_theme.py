import asyncpg

# ✅ Обновление прогресса по темам и уровням для одного клиента (используется после викторины)
async def update_user_progress_by_theme(conn: asyncpg.Connection, client_id: int):
    await conn.execute("""
        DELETE FROM user_progress_by_theme WHERE client_id = $1;
    """, client_id)

    await conn.execute("""
        INSERT INTO user_progress_by_theme (
            client_id, cat_id, total_words, learned_words, percent_done
        )
        SELECT
            $1 AS client_id,
            d.cat_id,
            COUNT(*) AS total_words,
            COUNT(lw.word_id) AS learned_words,
            ROUND(COUNT(lw.word_id) * 1.0 / COUNT(*)::numeric, 2) AS percent_done
        FROM dictionary d
        LEFT JOIN learned_words lw ON lw.word_id = d.word_id AND lw.client_id = $1
        WHERE d.cat_id IS NOT NULL
        GROUP BY d.cat_id;
    """, client_id)


# ✅ Обновление прогресса по всем пользователям (без уровней)
async def refresh_user_progress(conn: asyncpg.Connection):
    print("🟢 refresh_user_progress() вызван")
    try:
        async with conn.transaction():
            await conn.execute("TRUNCATE TABLE user_progress_by_theme")
            print("🧹 user_progress_by_theme очищена")

            # 🔹 Прогресс по темам (без учёта уровня)
            result = await conn.execute("""
                INSERT INTO user_progress_by_theme (
                    client_id, cat_id, total_words, learned_words, percent_done, updated_at
                )
                SELECT
                    lw.client_id,
                    d.cat_id,
                    COUNT(*) AS total_words,
                    COUNT(lw.word_id) AS learned_words,
                    ROUND(COUNT(lw.word_id) * 100.0 / NULLIF(COUNT(*), 0), 2) AS percent_done,
                    CURRENT_DATE
                FROM dictionary d
                JOIN learned_words lw ON lw.word_id = d.word_id
                WHERE d.cat_id IS NOT NULL
                GROUP BY lw.client_id, d.cat_id
            """)
            print(f"🟢 user_progress_by_theme обновлён: {result}")
    except Exception as e:
        print(f"❌ Ошибка при обновлении user_progress_by_theme: {e}")