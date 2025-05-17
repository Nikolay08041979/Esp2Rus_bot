import asyncpg
from datetime import datetime
from core.config import DB, LEVEL_CALCULATION_ONLINE
from db.create.archive.create_client_activity_words import ensure_client_activity_words_table
from analytics.metrics.calculate_quiz_weight import calculate_quiz_weight_with_fetch
from analytics.personalization.update_learned_words import update_learned_words
from analytics.personalization.update_user_progress_by_theme import update_user_progress_by_theme
from analytics.metrics.calculate_level_current import calculate_level_current
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



async def save_activity(data: dict):
    try:
        conn = await asyncpg.connect(**DB)

        result = await conn.fetchrow("SELECT client_id FROM client_info WHERE tg_id = $1", data["tg_id"])
        if result:
            client_id = result["client_id"]
        else:
            row = await conn.fetchrow("""
                INSERT INTO client_info (
                    tg_id, username, first_name, last_name,
                    date_reg, language_code
                )
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING client_id
            """, data["tg_id"], data["username"], data["first_name"], data["last_name"],
                  datetime.now().date(), data["language_code"])
            client_id = row["client_id"]

            # Пересоздание view из внешнего SQL-файла
            with open("db/create/personalized_words.sql", "r") as f:
                sql_view = f.read()
            await conn.execute(sql_view)

        quiz_weight = data.get("quiz_weight")
        if data["level_id_word"] is None and "words" in data and data["score_quiz"] == 1.0:
            word_srcs = [w["word_src"] for w in data["words"]]
            quiz_weight = await calculate_quiz_weight_with_fetch(conn, word_srcs, data["score_quiz"])
            data["quiz_weight"] = quiz_weight

        time_start = datetime.now().time()
        time_finish = datetime.now().time()

        await conn.execute("""
            INSERT INTO client_activity_log (
                client_id, date_login, time_start, time_finish,
                score_quiz, words_correct_quiz, words_incorrect_quiz,
                level_id_word, quiz_weight
            ) VALUES (
                $1, $2, $3, $4,
                $5, $6, $7,
                $8, $9
            )
        """, client_id,
            datetime.now().date(), time_start, time_finish,
            data["score_quiz"], data["words_correct_quiz"], data["words_incorrect_quiz"],
            data["level_id_word"], data.get("quiz_weight", None)
        )

        if LEVEL_CALCULATION_ONLINE:
            level_id_current = await calculate_level_current(conn, client_id)
            if level_id_current:
                await conn.execute(
                    "UPDATE client_analytics SET level_id_current = $1 WHERE client_id = $2",
                    level_id_current, client_id
                )

        await ensure_client_activity_words_table(conn)

        word_records = data.get("words", [])
        if word_records:
            row = await conn.fetchrow("""
                SELECT id FROM client_activity_log
                WHERE client_id = $1 AND time_start = $2 AND time_finish = $3
                ORDER BY id DESC LIMIT 1
            """, client_id, time_start, time_finish)
            activity_id = row["id"]

            word_srcs = [w["word_src"] for w in word_records]
            word_rows = await conn.fetch(
                "SELECT word_id, word_src FROM dictionary WHERE word_src = ANY($1)", word_srcs
            )
            esp_to_id = {row["word_src"]: row["word_id"] for row in word_rows}

            word_pairs = []
            for w in word_records:
                word_id = esp_to_id.get(w["word_src"])
                if word_id is not None:
                    is_correct = (
                        w.get("user_answer", "").strip().lower() ==
                        w.get("word_target", "").strip().lower()
                    )
                    word_pairs.append((activity_id, word_id, is_correct))

            await conn.executemany(
                "INSERT INTO client_activity_words (activity_id, word_id, is_correct) VALUES ($1, $2, $3)",
                word_pairs
            )

        await update_learned_words(conn, client_id)
        await update_user_progress_by_theme(conn, client_id)

        print(f"[ACTIVITY] Сессия клиента {client_id} сохранена. quiz_weight={quiz_weight}")

    except Exception as e:
        print(f"[ERROR] Ошибка в save_activity: {e}")
    finally:
        await conn.close()