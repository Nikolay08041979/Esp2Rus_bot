
# 📄 save_client_activity_log.py

"""
Модуль логирования клиентской сессии: client_activity_log + client_activity_words

Вызывается сразу после прохождения викторины.
"""

import asyncio
from datetime import datetime
from analytics import log_client_activity  # основной логгер v2

async def save_activity(data: dict):
    time_start = datetime.now().time()
    await asyncio.sleep(1)  # имитация работы
    time_finish = datetime.now().time()

    await log_client_activity(time_start, time_finish, data)

# Пример использования (удалить в проде):
if __name__ == "__main__":
    sample_data = {
        "tg_id": 123456,
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "language_code": "en",
        "score_quiz": 1.0,
        "words_correct_quiz": 10,
        "words_incorrect_quiz": 0,
        "level_id_word": None,
        "quiz_weight": None,
        "words": [
            {"word_esp": "libro"},
            {"word_esp": "comida"},
            {"word_esp": "grande"}
        ]
    }

    asyncio.run(save_activity(sample_data))
