
# 📄 analytics/metrics/get_level_id_word.py

"""
Возвращает level_id_word (уровень слов) из таблицы study_levels
по названию уровня на русском (например, "начальный", "средний", "продвинутый").

Если выбран режим "все уровни" — возвращает None
"""

import asyncpg

async def get_level_id_word_from_db(conn: asyncpg.Connection, level_name: str) -> int | None:
    if not level_name or level_name.lower() == "все уровни":
        return None

    row = await conn.fetchrow(
        "SELECT level_id FROM study_levels WHERE LOWER(level_word) = $1",
        level_name.lower()
    )
    return row["level_id"] if row else None
