import json
import psycopg2
from psycopg2.extras import execute_batch

def import_words_from_json(json_path: str, db_config: dict) -> dict:
    """Импортирует слова из JSON-файла в БД и возвращает отчёт."""
    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)

    success_count = 0
    errors = []
    duplicates = []

    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    def get_id(table, column, value):
        cur.execute(f"SELECT id FROM (SELECT cat_id as id, cat_name as name FROM word_category UNION ALL SELECT lev_id, lev_name FROM study_level) sub WHERE LOWER(name) = LOWER(%s)", (value,))
        res = cur.fetchone()
        if res:
            return res[0]
        raise ValueError(f"{value} не найден в {table}")

    for entry in data:
        # Приводим все значения к нижнему регистру для единообразия хранения
        entry['word_esp'] = entry['word_esp'].strip().lower()
        entry['word_rus'] = entry['word_rus'].strip().lower()
        entry['category'] = entry['category'].strip().lower()
        entry['level'] = entry['level'].strip().lower()
        try:
            other_rus = entry['other_rus'].split(',')
            if len(other_rus) != 3:
                raise ValueError("other_rus должен содержать 3 значения")

            # Проверка на дубликат (без учёта регистра)
            cur.execute("SELECT word_id FROM esp2rus_dictionary WHERE LOWER(word_esp) = LOWER(%s)", (entry['word_esp'],))
            if cur.fetchone():
                duplicates.append(entry['word_esp'])
                continue

            cat_id = get_id('word_category', 'cat_name', entry['category'])
            lev_id = get_id('study_level', 'lev_name', entry['level'])

            cur.execute(
                """INSERT INTO esp2rus_dictionary
                (word_esp, word_rus, other_rus1, other_rus2, other_rus3, cat_id, lev_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    entry['word_esp'],
                    entry['word_rus'],
                    other_rus[0],
                    other_rus[1],
                    other_rus[2],
                    cat_id,
                    lev_id
                )
            )
            success_count += 1

        except Exception as e:
            errors.append(f"{entry.get('word_esp', '?')}: {str(e)}")

    conn.commit()
    cur.close()
    conn.close()

    return {
        "added": success_count,
        "duplicates": duplicates,
        "errors": errors
    }