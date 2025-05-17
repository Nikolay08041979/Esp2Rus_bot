# 📐 calculate_level_current.py — обновлённая логика присвоения CEFR уровня

import asyncpg

# 📌 Расчёт текущего уровня владения языком на основе прогресса
# Прогресс (coverage) считается по таблице learned_words / dictionary
# Уровень присваивается, если выполнены условия из level_matrix по coverage
# Точность (accuracy) больше НЕ используется (исключена по решению от 2025-05-14)

async def calculate_level_current(conn: asyncpg.Connection, client_id: int) -> int | None:
    # Получаем список всех уровней из матрицы
    rows = await conn.fetch("""
        SELECT level_id_client, lev_id, min_coverage
        FROM level_matrix
        ORDER BY level_id_client
    """)

    level_id_current = None

    for row in rows:
        level_id = row["level_id_client"]
        lev_id = row["lev_id"]
        min_coverage = row["min_coverage"]

        # Получаем общее число слов и выученных слов по этому уровню
        stats = await conn.fetchrow("""
            SELECT
                COUNT(*) AS total,
                COUNT(lw.word_id) AS learned
            FROM dictionary d
            LEFT JOIN learned_words lw ON lw.word_id = d.word_id AND lw.client_id = $1
            WHERE d.lev_id = $2
        """, client_id, lev_id)

        total = stats["total"] or 0
        learned = stats["learned"] or 0

        if total == 0:
            continue

        coverage = round((learned / total) * 100, 2)

        print(f"[DEBUG] Клиент {client_id}: lev_id={lev_id}, coverage={coverage:.2f}%", end=" ")

        if coverage >= min_coverage:
            level_id_current = level_id
            print(
                f"[DEBUG] Клиент {client_id}: lev_id={lev_id}, coverage={coverage:.2f}% ✅ присвоен уровень level_id={level_id}")
        else:
            print(
                f"[DEBUG] Клиент {client_id}: lev_id={lev_id}, coverage={coverage:.2f}% ❌ недостаточно для уровня level_id={level_id}")

    # Обновляем уровень в client_analytics
    await conn.execute("""
        UPDATE client_analytics
        SET level_id_current = $2
        WHERE client_id = $1
    """, client_id, level_id_current)

    if level_id_current:
        return level_id_current
    else:
        print(f"[DEBUG] Клиент client_id={client_id}: уровень не присвоен. Текущий уровень = 0")
        return None
