# simulate_bulk_upload_test.py — расширенный стресс-тест + режим точного уровня
import asyncio
import asyncpg
from datetime import datetime
from core.config import DB
from analytics.reports.generate_user_report import generate_user_report
from analytics.metrics.calculate_level_current import calculate_level_current
import random
import os

MODE = "targeted"
LOG_PATH = "logs/simulate_test.log"
os.makedirs("logs", exist_ok=True)

def log(msg):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | {msg}\n")
    print(msg)

TEST_WORD_COUNT = 100
TEST_CLIENTS = 3
QUIZZES_PER_CLIENT = 30
WORDS_PER_QUIZ = 3

TEST_CATEGORIES = ['природа', 'транспорт', 'еда']
TEST_LEV_IDS = [1, 2, 3]

async def insert_test_words(conn):
    log("🧹 Удаляем предыдущие тестовые слова...")
    await conn.execute("DELETE FROM learned_words WHERE word_id IN (SELECT word_id FROM dictionary WHERE word_src LIKE 'stress_word_%')")
    await conn.execute("DELETE FROM client_activity_words WHERE word_id IN (SELECT word_id FROM dictionary WHERE word_src LIKE 'stress_word_%')")
    await conn.execute("DELETE FROM dictionary WHERE word_src LIKE 'stress_word_%'")

    log(f"📥 Загружаем {TEST_WORD_COUNT} тестовых слов в dictionary...")
    for i in range(TEST_WORD_COUNT):
        category = TEST_CATEGORIES[i % len(TEST_CATEGORIES)]
        level_id = TEST_LEV_IDS[i % len(TEST_LEV_IDS)]
        await conn.execute(
            '''
            INSERT INTO dictionary (word_src, word_rus, other_rus1, other_rus2, other_rus3, cat_id, lev_id)
            VALUES ($1, $2, $3, $4, $5,
                (SELECT cat_id FROM word_category WHERE cat_name = $6 LIMIT 1),
                $7
            )
            ''',
            f"stress_word_{i}",
            f"стресс_{i}",
            f"сино1_{i}",
            f"сино2_{i}",
            f"сино3_{i}",
            category,
            level_id
        )
    log("✅ Слова добавлены успешно.")

async def create_test_clients(conn):
    log("👤 Создаём тестовых клиентов...")
    client_ids = []
    for i in range(TEST_CLIENTS):
        tg_id = 990000000 + i
        username = f"stress_bot_{i}"
        await conn.execute(
            '''
            INSERT INTO client_info (tg_id, username, first_name, last_name, date_reg)
            VALUES ($1, $2, $3, $4, CURRENT_DATE)
            ON CONFLICT (tg_id) DO NOTHING
            ''',
            tg_id, username, f"Stress{i}", f"User{i}"
        )
        row = await conn.fetchrow("SELECT client_id FROM client_info WHERE tg_id = $1", tg_id)
        client_ids.append((tg_id, row["client_id"]))
    log(f"✅ Клиенты: {client_ids}")
    return client_ids

async def simulate_quiz(conn, client_id, level_id, perfect=True):
    word_rows = await conn.fetch(
        "SELECT word_id FROM dictionary WHERE lev_id = $1 ORDER BY RANDOM() LIMIT $2",
        level_id, WORDS_PER_QUIZ
    )
    correct = WORDS_PER_QUIZ if perfect else random.randint(1, WORDS_PER_QUIZ - 1)
    incorrect = WORDS_PER_QUIZ - correct

    now = datetime.now()
    await conn.execute(
        '''
        INSERT INTO client_activity_log (
            client_id, date_login, time_start, time_finish,
            score_quiz, words_correct_quiz, words_incorrect_quiz,
            level_id_word, quiz_weight
        )
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        ''',
        client_id,
        now.date(),
        now.time(),
        now.time(),
        correct / WORDS_PER_QUIZ,
        correct,
        incorrect,
        level_id,
        1.0
    )

    activity_id = await conn.fetchval("SELECT MAX(id) FROM client_activity_log WHERE client_id = $1", client_id)
    for row in word_rows:
        await conn.execute(
            '''
            INSERT INTO client_activity_words (activity_id, word_id, is_correct)
            VALUES ($1, $2, TRUE)
            ON CONFLICT DO NOTHING
            ''',
            activity_id, row["word_id"]
        )
        await conn.execute(
            '''
            INSERT INTO learned_words (client_id, word_id, learned_at)
            VALUES ($1, $2, CURRENT_DATE)
            ON CONFLICT DO NOTHING
            ''',
            client_id, row["word_id"]
        )

async def main():
    log(f"🚀 Расширенный тест MODE = {MODE}")
    conn = await asyncpg.connect(**DB)
    try:
        await insert_test_words(conn)
        clients = await create_test_clients(conn)

        for idx, (tg_id, client_id) in enumerate(clients):
            for i in range(QUIZZES_PER_CLIENT):
                level_id = random.choice(TEST_LEV_IDS)
                perfect = idx == 0 or i % 2 == 0  # клиент 0 — идеальный, остальные с ошибками
                await simulate_quiz(conn, client_id, level_id, perfect)

            level = await calculate_level_current(conn, client_id)
            log(f"📊 TG {tg_id} — level_id_current = {level}")
            report = await generate_user_report(tg_id)
            log(f"📝 Отчёт TG {tg_id}:\n" + report + "\n" + "="*60)

    finally:
        await conn.close()
        log("✅ Тест завершён")

if __name__ == "__main__":
    asyncio.run(main())
