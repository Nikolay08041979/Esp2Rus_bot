# 📐 analytics/metrics/calculate_quiz_weight.py

"""
Модуль расчёта quiz_weight:
1. calculate_quiz_weight(...) — чистая формула
2. calculate_quiz_weight_with_fetch(...) — достаёт веса из view_word_weight и вызывает расчёт
3. calculate_quiz_weight_by_level(...) — достаёт вес по level_id_word из view_quiz_weight_by_group и умножает на количество правильных слов
"""

from typing import Optional
import asyncpg

# 💡 коэффициент: вес одного правильного слова
WORD_CORRECT_VALUE = 0.1


# 1️⃣ Чистая формула
def calculate_quiz_weight(word_srcs: list[str], score_quiz: float, word_weights: dict[str, float]) -> Optional[float]:
    if score_quiz < 1.0:
        return None

    unique_words = set(word_srcs)
    weights = [word_weights.get(word, 1.0) for word in unique_words]

    if not weights:
        return None

    result = round(sum(weights) / len(weights), 2)
    return result


# 2️⃣ Вытаскиваем веса по словам
async def calculate_quiz_weight_with_fetch(conn: asyncpg.Connection, word_srcs: list[str], score_quiz: float) -> Optional[float]:
    if score_quiz < 1.0 or not word_srcs:
        return None

    rows = await conn.fetch(
        "SELECT word_src, weight_value FROM view_word_weight WHERE word_src = ANY($1)", word_srcs
    )
    word_weights = {row["word_src"]: float(row["weight_value"]) for row in rows}

    return calculate_quiz_weight(word_srcs, score_quiz, word_weights)


# 3️⃣ Расчёт веса по уровню + множитель за кол-во правильных слов
async def calculate_quiz_weight_by_level(conn: asyncpg.Connection, lev_id: int, score_quiz: float, words_correct_quiz: int) -> Optional[float]:
    """
    Возвращает quiz_weight = базовый вес * (words_correct_quiz * WORD_CORRECT_VALUE), если quiz пройден на 100%
    """
    if score_quiz < 1.0:
        return None

    try:
        row = await conn.fetchrow(
            "SELECT weight_value FROM view_quiz_weight_by_group WHERE lev_id = $1",
            lev_id
        )
        if not row:
            return None

        base_weight = float(row["weight_value"])
        multiplier = words_correct_quiz * WORD_CORRECT_VALUE
        quiz_weight = round(base_weight * multiplier, 2)

        return quiz_weight

    except Exception as e:
        print(f"[ERROR] calculate_quiz_weight_by_level failed: {e}")
        return None