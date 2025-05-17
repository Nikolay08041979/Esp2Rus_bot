# 📄 db/views/create_view_word_weight.py
# 📄 db/views/create_view_word_weight.py

import asyncpg
import asyncio
from core.config import DB  # централизованный config с подключением к БД

VIEW_NAME = "view_word_weight"

DROP_VIEW_SQL = f"DROP VIEW IF EXISTS {VIEW_NAME} CASCADE;"

CREATE_VIEW_SQL = f"""
CREATE VIEW {VIEW_NAME} AS
SELECT
    d.word_id,
    d.word_src,
    d.lev_id,
    sl.weight_value
FROM dictionary d
JOIN study_level sl_map ON d.lev_id = sl_map.lev_id
JOIN study_levels sl ON sl_map.lev_name = sl.level_word
WHERE sl.weight_value IS NOT NULL;
"""

async def create_view():
    print(f"🔧 Подключаемся к базе для пересоздания VIEW: {VIEW_NAME}")
    conn = await asyncpg.connect(**DB)
    try:
        await conn.execute(DROP_VIEW_SQL)
        print(f"🗑️ Старый VIEW {VIEW_NAME} удалён (если существовал).")
        await conn.execute(CREATE_VIEW_SQL)
        print(f"✅ VIEW {VIEW_NAME} успешно создан.")
    except Exception as e:
        print(f"❌ Ошибка при создании VIEW {VIEW_NAME}: {e}")
    finally:
        await conn.close()
        print("🔌 Соединение с БД закрыто.")

if __name__ == "__main__":
    asyncio.run(create_view())
