import json
import psycopg2
from core.config import DB

with open('../data/words.json', encoding='utf-8') as f:
    data = json.load(f)

conn = psycopg2.connect(**DB)

cur = conn.cursor()

def get_id(table, value):
    if table == 'word_category':
        id_column = 'cat_id'
        name_column = 'cat_name'
    elif table == 'study_level':
        id_column = 'lev_id'
        name_column = 'lev_name'
    else:
        raise ValueError("Unknown table")

    cur.execute(f"SELECT {id_column} FROM {table} WHERE LOWER({name_column}) = LOWER(%s)", (value,))
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        raise ValueError(f"{value} not found in {table}")

added = 0
skipped = 0

for entry in data:
    # Приводим все значения к нижнему регистру для единообразия хранения
    entry['word_esp'] = entry['word_esp'].strip().lower()
    entry['word_rus'] = entry['word_rus'].strip().lower()
    entry['category'] = entry['category'].strip().lower()
    entry['level'] = entry['level'].strip().lower()
    other_rus = entry['other_rus'].split(',')
    cat_id = get_id('word_category', entry['category'])
    lev_id = get_id('study_level', entry['level'])

    cur.execute("SELECT 1 FROM esp2rus_dictionary WHERE LOWER(word_esp) = LOWER(%s)", (entry['word_esp'],))
    if cur.fetchone():
        skipped += 1
        continue

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
    added += 1

conn.commit()
cur.close()
conn.close()

print(f"✅ Импорт завершён. Добавлено: {added}, Пропущено (дубликаты): {skipped}")