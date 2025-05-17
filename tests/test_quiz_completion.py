
import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock

from analytics.analytics import log_client_activity
from analytics.metrics.calculate_quiz_weight import calculate_quiz_weight
from analytics.metrics.get_level_id_word import get_level_id_word

@pytest.mark.asyncio
async def test_quiz_completion_logic(monkeypatch):
    # Подмена логгера и логгера активности
    monkeypatch.setattr("analytics.analytics.log_client_activity", AsyncMock())

    # Мокаем состояние FSM
    mock_state = AsyncMock()
    mock_state.get_data.return_value = {
        "words": [
            {"word_esp": "el gato", "word_rus": "кот", "level_id_word": 1},
            {"word_esp": "el perro", "word_rus": "собака", "level_id_word": 1},
        ],
        "score": 2,
        "index": 2,  # <-- Важно! index == len(words)
        "level": "начальный",
        "time_start": (datetime.now() - timedelta(minutes=5)).time()
    }

    class MockUser:
        id = 1
        username = "testuser"
        first_name = "Имя"
        last_name = "Фамилия"
        language_code = "ru"

    class MockMessage:
        from_user = MockUser()
        logs = []

        async def answer(self, text, reply_markup=None):
            self.logs.append(text)

    message = MockMessage()

    # Импортируем нужные функции
    level = "начальный"
    data = await mock_state.get_data()
    words = data["words"]
    score = data["score"]
    level_id_word = get_level_id_word(level)
    quiz_weight = calculate_quiz_weight([w["level_id_word"] for w in words])
    time_finish = datetime.now().time()
    time_start = data.get("time_start", time_finish)

    await message.answer(
        f"Тренировка окончена! Ваш результат: {int(100 * (score / len(words)))}% \n"
        f"({score} правильных ответов из {len(words)}).\n\n"
        + ("🎉 Поздравляем!" if score == len(words) else "🎯 Ты почти у цели!")
    )

    await log_client_activity(time_start, time_finish, {
        "tg_id": message.from_user.id,
        "username": message.from_user.username,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "language_code": message.from_user.language_code,
        "score_quiz": round(score / len(words), 2),
        "words_correct_quiz": score,
        "words_incorrect_quiz": len(words) - score,
        "level_id_word": level_id_word,
        "quiz_weight": quiz_weight
    })

    # Проверка, что финальное сообщение отправлено
    assert any("Тренировка окончена!" in t for t in message.logs)
