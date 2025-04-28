import asyncpg
from core.config import DB

async def get_all_categories() -> list[str]:
    conn = await asyncpg.connect(**DB)
    rows = await conn.fetch("SELECT cat_name FROM word_category ORDER BY cat_name")
    await conn.close()
    return [r["cat_name"] for r in rows]

async def get_all_levels() -> list[str]:
    conn = await asyncpg.connect(**DB)
    rows = await conn.fetch("SELECT lev_name FROM study_level ORDER BY lev_name")
    await conn.close()
    return [r["lev_name"] for r in rows]

async def get_words_for_quiz(category: str, level: str | None, limit: int) -> list[dict]:
    conn = await asyncpg.connect(**DB)

    if level and level.lower().strip() != "все уровни":
        query = '''
            SELECT d.word_esp, d.word_rus, d.other_rus1, d.other_rus2, d.other_rus3
            FROM esp2rus_dictionary d
            JOIN word_category c ON d.cat_id = c.cat_id
            LEFT JOIN study_level l ON d.lev_id = l.lev_id
            WHERE LOWER(c.cat_name) = LOWER($1) AND LOWER(l.lev_name) = LOWER($2)
            ORDER BY random()
            LIMIT $3
        '''
        rows = await conn.fetch(query, category, level, limit)
    else:
        query = '''
            SELECT d.word_esp, d.word_rus, d.other_rus1, d.other_rus2, d.other_rus3
            FROM esp2rus_dictionary d
            JOIN word_category c ON d.cat_id = c.cat_id
            WHERE LOWER(c.cat_name) = LOWER($1)
            ORDER BY random()
            LIMIT $2
        '''
        rows = await conn.fetch(query, category, limit)

    await conn.close()
    return [dict(r) for r in rows]


async def get_category_stats() -> list[dict]:
    query = '''
        SELECT c.cat_name AS категория, COALESCE(COUNT(d.word_id), 0) AS количество_слов
        FROM word_category c
        LEFT JOIN esp2rus_dictionary d ON c.cat_id = d.cat_id
        GROUP BY c.cat_name
        ORDER BY количество_слов DESC
    '''
    conn = await asyncpg.connect(**DB)
    rows = await conn.fetch(query)
    await conn.close()
    return [dict(r) for r in rows]


async def add_category(name: str) -> str:
    name = name.strip().lower()
    query = 'INSERT INTO word_category (cat_name) VALUES (LOWER($1)) ON CONFLICT DO NOTHING'
    conn = await asyncpg.connect(**DB)
    await conn.execute(query, name)
    await conn.close()
    return f"✅ Категория '{name.lower()}' добавлена (если её не было ранее)."


async def get_all_levels_text() -> list[str]:
    query = 'SELECT lev_name FROM study_level ORDER BY lev_name'
    conn = await asyncpg.connect(**DB)
    rows = await conn.fetch(query)
    await conn.close()
    return [r["lev_name"] for r in rows]

async def add_level(name: str) -> str:
    name = name.strip().lower()
    query = 'INSERT INTO study_level (lev_name) VALUES (LOWER($1)) ON CONFLICT DO NOTHING'
    conn = await asyncpg.connect(**DB)
    await conn.execute(query, name)
    await conn.close()
    return f"✅ Уровень '{name.lower()}' добавлен (если не существовал)."


async def delete_category(name: str) -> str:
    name = name.strip().lower()
    conn = await asyncpg.connect(**DB)
    await conn.execute(
        '''
        DELETE FROM esp2rus_dictionary
        WHERE cat_id = (SELECT cat_id FROM word_category WHERE LOWER(cat_name) = LOWER($1))
        ''',
        name
    )
    await conn.execute(
        '''
        DELETE FROM word_category
        WHERE LOWER(cat_name) = LOWER($1)
        ''',
        name
    )
    await conn.close()
    return f"🗑 Категория '{name}' и связанные слова удалены."

async def delete_level(name: str) -> str:
    name = name.strip().lower()
    conn = await asyncpg.connect(**DB)
    await conn.execute(
        '''
        DELETE FROM esp2rus_dictionary
        WHERE lev_id = (SELECT lev_id FROM study_level WHERE LOWER(lev_name) = LOWER($1))
        ''',
        name
    )
    await conn.execute(
        '''
        DELETE FROM study_level
        WHERE LOWER(lev_name) = LOWER($1)
        ''',
        name
    )
    await conn.close()
    return f"🗑 Уровень '{name}' и связанные слова удалены."

async def get_level_stats() -> list[dict]:
    query = '''
        SELECT l.lev_name AS уровень, COALESCE(COUNT(d.word_id), 0) AS количество_слов
        FROM study_level l
        LEFT JOIN esp2rus_dictionary d ON l.lev_id = d.lev_id
        GROUP BY l.lev_name
        ORDER BY количество_слов DESC
    '''
    conn = await asyncpg.connect(**DB)
    rows = await conn.fetch(query)
    await conn.close()
    return [dict(r) for r in rows]