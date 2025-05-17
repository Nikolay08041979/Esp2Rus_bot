# 📄 db/views/create_view_quiz_weight_by_group.py

import asyncpg
import asyncio
from core.config import DB  # централизованная конфигурация подключения к БД

VIEW_NAME = "view_quiz_weight_by_group"

CREATE_VIEW_SQL = f"""
CREATE OR REPLACE VIEW {VIEW_NAME} AS
SELECT
    vslm.lev_id,                         -- 1 — начальный, 2 — средний, 3 — продвинутый
    MAX(sl.weight_value) AS weight_value -- Максимальный вес в рамках группы (можно заменить на AVG)
FROM view_study_level_mapped vslm
JOIN study_levels sl ON sl.level_word = vslm.level_word
GROUP BY vslm.lev_id
ORDER BY vslm.lev_id;
"""

async def create_view():
    conn = await asyncpg.connect(**DB)
    try:
        await conn.execute(CREATE_VIEW_SQL)
        print(f"✅ VIEW {VIEW_NAME} успешно создана или обновлена.")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(create_view())
