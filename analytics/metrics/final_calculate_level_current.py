# 📐 calculate_level_current.py

import asyncpg

async def calculate_level_current(conn: asyncpg.Connection, client_id: int) -> int | None:
    """
    Возвращает level_id_current (1–6) для клиента, если выполнены условия по охвату и точности
    """
    # Шаг 1: Получить список всех уровней из level_matrix
    level_rows = await conn.fetch(
        "SELECT level_id_client, required_coverage, required_accuracy "
        "FROM level_matrix ORDER BY level_id_client ASC"
    )

    for row in level_rows:
        target_level = row["level_id_client"]
        required_coverage = row["required_coverage"]
        required_accuracy = row["required_accuracy"]

        # Шаг 2: Получить общее количество слов по этому уровню
        total_words_row = await conn.fetchrow(
            "SELECT COUNT(*) as total FROM dictionary "
            "WHERE lev_id = (SELECT lev_id FROM study_level WHERE lev_name = ("
            "SELECT level_word FROM study_levels WHERE level_id = $1))",
            target_level
        )
        total_words = total_words_row["total"] if total_words_row else 0
        if total_words == 0:
            continue

        # Шаг 3: Получить количество выученных слов клиента
        learned_row = await conn.fetchrow(
            "SELECT COUNT(*) as learned FROM learned_words lw "
            "JOIN dictionary d ON lw.word_id = d.word_id "
            "WHERE lw.client_id = $1 AND d.lev_id = ("
            "SELECT lev_id FROM study_level WHERE lev_name = ("
            "SELECT level_word FROM study_levels WHERE level_id = $2))",
            client_id, target_level
        )
        learned = learned_row["learned"] if learned_row else 0
        coverage_pct = (learned / total_words) * 100

        if coverage_pct < required_coverage:
            continue

        # Шаг 4: Проверить точность по этому уровню
        accuracy_row = await conn.fetchrow(
            "SELECT SUM(words_correct_quiz)::float / NULLIF(SUM(words_correct_quiz + words_incorrect_quiz), 0) * 100 AS accuracy "
            "FROM client_activity_log "
            "WHERE client_id = $1 AND level_id_word = $2",
            client_id, target_level
        )
        accuracy = accuracy_row["accuracy"] if accuracy_row else 0
        if accuracy is None or accuracy < required_accuracy:
            continue
        print(f"[DEBUG] Уровень присвоен клиенту <client_id>: покрытие=<coverage>%, точность=<accuracy>%")

        return target_level  # ✅ Все условия выполнены

    return None  # ❌ Ни один уровень не подошёл