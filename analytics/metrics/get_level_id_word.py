
# 📄 analytics/metrics/get_level_id_word.py

"""
Возвращает level_id_word (уровень слов) из таблицы study_levels
по названию уровня на русском (например, "начальный", "средний", "продвинутый").

Если выбран режим "все уровни" — возвращает None.
Подключение к БД осуществляется внутри функции.
"""

import asyncpg
from core.config import DB

async def get_level_id_word(level_name: str) -> int | None:
    if not level_name or level_name.lower() == "все уровни":
        return None

    try:
        conn = await asyncpg.connect(**DB)
        row = await conn.fetchrow(
            "SELECT level_id FROM study_levels WHERE LOWER(level_word) = $1",
            level_name.lower()
        )
        await conn.close()
        return row["level_id"] if row else None
    except Exception as e:
        print(f"[ERROR] get_level_id_word failed: {e}")
        return None
