import json
import asyncpg
from core.config import DB

async def import_words_from_json(json_path: str, db_params: dict) -> dict:
    """Импорт слов из JSON-файла в базу данных"""

    with open(json_path, "r", encoding="utf-8") as f:
        words = json.load(f)

    added = 0
    duplicates = []
    errors = []
    added_words = []

    conn = await asyncpg.connect(**db_params)

    for word in words:
        try:
            word_src = word.get("word_src", "").strip().lower()
            word_rus = word.get("word_rus", "").strip().lower()
            category = word.get("category", "").strip().lower()
            level = word.get("level", None)
            other_rus1 = word.get("other_rus1")
            other_rus2 = word.get("other_rus2")
            other_rus3 = word.get("other_rus3")

            if not word_src or not word_rus or not category:
                errors.append(word)
                continue

            # Проверка наличия слова
            existing = await conn.fetchrow("""
                SELECT * FROM dictionary d
                JOIN word_category c ON d.cat_id = c.cat_id
                WHERE d.word_src = $1
            """, word_src)

            if existing:
                existing_category = existing["cat_name"].strip().lower()
                if existing_category == category:
                    duplicates.append(word)
                    continue  # Дубликат в той же категории
                else:
                    # Возможен конфликт категорий
                    duplicates.append(word)
                    continue

            # Проверка существования категории
            cat = await conn.fetchrow("SELECT cat_id FROM word_category WHERE LOWER(cat_name) = LOWER($1)", category)
            if not cat:
                cat_id = await conn.fetchval(
                    "INSERT INTO word_category (cat_name) VALUES ($1) RETURNING cat_id", category
                )
            else:
                cat_id = cat["cat_id"]

            # Проверка существования уровня
            lev_id = None
            if level:
                lev = await conn.fetchrow("SELECT lev_id FROM study_level WHERE LOWER(lev_name) = LOWER($1)", level)
                if not lev:
                    lev_id = await conn.fetchval(
                        "INSERT INTO study_level (lev_name) VALUES ($1) RETURNING lev_id", level
                    )
                else:
                    lev_id = lev["lev_id"]

            # Добавление нового слова
            await conn.execute("""
                INSERT INTO dictionary (word_src, word_rus, cat_id, lev_id, other_rus1, other_rus2, other_rus3)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
            """, word_src, word_rus, cat_id, lev_id, other_rus1, other_rus2, other_rus3)

            added += 1
            added_words.append(word_src)

        except Exception as e:
            errors.append({"word": word, "error": str(e)})

    await conn.close()

    return {
        "added": added,
        "duplicates": duplicates,
        "errors": errors,
        "added_words": added_words
    }