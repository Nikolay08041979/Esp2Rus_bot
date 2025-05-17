
# 🧠 Матрица присвоения уровня (level_id_client) согласно CEFR:
# 1 — A1: >= 50% слов уровня A1 с результатом 100%
# 2 — A2: >= 100% слов уровня A1 с результатом 100%
# 3 — B1: >= 50% слов уровня B с результатом 100%
# 4 — B2: >= 100% слов уровня B с результатом 100%
# 5 — C1: >= 50% слов уровня C с результатом 100%
# 6 — C2: >= 100% слов уровня C с результатом 100%
#
# Важно: уровень присваивается только если пройдено необходимое количество слов с quiz_weight != NULL

# Пример логики (в упрощённой форме, реализуется в коде ниже):
# SELECT COUNT(*) FROM esp2rus_dictionary WHERE lev_id = 1;
# SELECT COUNT(*) FROM client_activity_words JOIN ... WHERE lev_id = 1 AND score = 1.0;


from asyncpg import Connection
from datetime import datetime

LEVEL_THRESHOLD_COVERAGE = 0.8  # ≥ 80% слов пройдено
LEVEL_THRESHOLD_SCORE = 0.8     # ≥ 80% точность

async def update_level_current(conn: Connection, client_id: int) -> None:
    # Шаг 1: получаем охват и точность по каждому уровню клиента
    query = """
        SELECT
            level_id_word,
            COUNT(*) AS quizzes_passed,
            SUM(score_quiz * quiz_weight) / NULLIF(SUM(quiz_weight), 0) AS avg_score
        FROM client_activity_log
        WHERE client_id = $1
        GROUP BY level_id_word
    """
    level_stats = await conn.fetch(query, client_id)

    if not level_stats:
        print(f"[LEVEL] Нет данных по активности клиента {client_id}")
        return

    # Шаг 2: получаем общее количество слов по уровням
    dictionary_totals = await conn.fetch("""
        SELECT lev_id, COUNT(*) AS total_words
        FROM esp2rus_dictionary
        WHERE lev_id IS NOT NULL
        GROUP BY lev_id
    """)

    total_words_map = {row["lev_id"]: row["total_words"] for row in dictionary_totals}

    # Шаг 3: ищем максимальный уровень, где выполнены оба условия
    qualified_levels = []

    for stat in level_stats:
        level_id = stat["level_id_word"]
        passed = stat["quizzes_passed"]
        avg_score = float(stat["avg_score"] or 0.0)
        total = total_words_map.get(level_id, 0)

        if total == 0:
            continue

        coverage_ratio = passed / total

        if coverage_ratio >= LEVEL_THRESHOLD_COVERAGE and avg_score >= LEVEL_THRESHOLD_SCORE:
            qualified_levels.append(level_id)

    if not qualified_levels:
        print(f"[LEVEL] У клиента {client_id} пока нет завершённых уровней")
        return

    new_level_id = max(qualified_levels)

    # Шаг 4: обновим client_analytics
    await conn.execute(
        """
        UPDATE client_analytics
        SET level_id_current = $1,
            date_level_upgraded = $2
        WHERE client_id = $3
        """,
        new_level_id,
        datetime.utcnow(),
        client_id
    )

    print(f"[LEVEL] Клиент {client_id} достиг уровня {new_level_id}")
