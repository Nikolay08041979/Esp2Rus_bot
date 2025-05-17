# db/create/create_client_activity_words.py

"""
Создаёт таблицу client_activity_words, если она не существует.
"""

async def ensure_client_activity_words_table(conn):
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS client_activity_words (
            id SERIAL PRIMARY KEY,
            activity_id INT NOT NULL REFERENCES client_activity_log(id) ON DELETE CASCADE,
            word_id INT NOT NULL REFERENCES dictionary(word_id) ON DELETE CASCADE
        );
    """)
