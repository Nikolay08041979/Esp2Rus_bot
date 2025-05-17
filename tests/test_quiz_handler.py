import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock

from archeved.analytics_old.analytics_v1_backup import log_client_activity
from archeved.calculate_quiz_weight import calculate_quiz_weight
from analytics.metrics.get_level_id_word import get_level_id_word

@pytest.mark.asyncio
async def test_process_quiz_end_logic(monkeypatch):
    # Мокаем log_client_activity чтобы не писать в БД
    monkeypatch.setattr("analytics.analytics.log_client_activity", AsyncMock())

    # Данные, имитирующие состояние FSM в конце викторины
    mock_state = AsyncMock()
    mock_state.get_data.return_value = {
        "words": [
            {"word_src": "el médico", "word_rus": "врач", "level_id_word": 2},
            {"word_src": "la casa", "word_rus": "дом", "level_id_word": 2},
        ],
        "score": 2,
        "index": 2,
        "level": "средний",
        "time_start": (datetime.now() - timedelta(minutes=5)).time()
    }

    # Мокаем message с пользователем
    class MockUser:
        id = 123
        username = "testuser"
        first_name = "Имя"
        last_name = "Фамилия"
        language_code = "ru"

    class MockMessage:
        from_user = MockUser()
        text = "любая строка"
        calls = []

        async def answer(self, text, reply_markup=None):
            self.calls.append(text)

    message = MockMessage()

    # Импортируем часть логики из process_quiz_answer
    data = await mock_state.get_data()
    words = data["words"]
    score = data["score"]
    level = data["level"]

    level_id_word = get_level_id_word(level)
    quiz_weight = calculate_quiz_weight([w.get("level_id_word", 1) for w in words])
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

    # Проверка, что сообщение с результатом отправлено
    assert any("Тренировка окончена!" in c for c in message.calls)
