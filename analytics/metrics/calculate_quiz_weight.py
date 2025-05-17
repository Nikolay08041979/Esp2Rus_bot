
# 📐 analytics/metrics/calculate_quiz_weight.py

"""
Модуль расчёта quiz_weight:
1. calculate_quiz_weight(...) — чистая формула
2. calculate_quiz_weight_with_fetch(...) — достаёт веса из view_word_weight и вызывает расчёт
"""

from typing import Optional
import asyncpg

# Чистая формула: рассчитывает вес по переданному словарю весов
def calculate_quiz_weight(word_srcs: list[str], score_quiz: float, word_weights: dict[str, float]) -> Optional[float]:
    if score_quiz < 1.0:
        return None

    unique_words = set(word_srcs)
    weights = [word_weights.get(word, 1.0) for word in unique_words]

    if not weights:
        return None

    result = round(sum(weights) / len(weights), 2)
    return result


# Обёртка: достаёт веса из view_word_weight по словам, вызывает чистую формулу
async def calculate_quiz_weight_with_fetch(conn: asyncpg.Connection, word_srcs: list[str], score_quiz: float) -> Optional[float]:
    if score_quiz < 1.0 or not word_srcs:
        return None

    rows = await conn.fetch(
        "SELECT word_src, weight_value FROM view_word_weight WHERE word_src = ANY($1)", word_srcs
    )
    word_weights = {row["word_src"]: float(row["weight_value"]) for row in rows}

    return calculate_quiz_weight(word_srcs, score_quiz, word_weights)
