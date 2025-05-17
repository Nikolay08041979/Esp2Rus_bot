
# 📄 analytics/metrics/calculate_client_rating.py

import asyncpg

async def get_client_rating(conn: asyncpg.Connection, client_id: int) -> float:
    """
    Возвращает суммарный рейтинг клиента как сумму quiz_weight по всем успешным викторинам.
    Если данных нет — возвращает 0.0
    """
    query = """
        SELECT SUM(quiz_weight) AS rating
        FROM client_activity_log
        WHERE client_id = $1 AND quiz_weight IS NOT NULL
    """
    row = await conn.fetchrow(query, client_id)

    if row and row["rating"]:
        rating = round(float(row["rating"]), 2)
    else:
        rating = 0.0

  #  print(f"[DEBUG] Расчёт client_rating для client_id={client_id}: {rating}")
    return rating
