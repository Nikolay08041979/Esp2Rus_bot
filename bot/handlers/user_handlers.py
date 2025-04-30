from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from bot.keyboards import category_keyboard, level_keyboard, answer_keyboard, start_over_keyboard
from bot.states import QuizState
from db.models import get_all_categories, get_all_levels, get_words_for_quiz, get_all_words
from random import shuffle

import logging
logger = logging.getLogger(__name__)

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    categories = await get_all_categories()
    keyboard = category_keyboard(categories)
    await message.answer("👋 Привет! Пожалуйста, выбери категорию слов:", reply_markup=keyboard)

@router.callback_query(F.data.startswith("cat:"))
async def category_selected(callback: CallbackQuery, state: FSMContext):
    category = callback.data.split("cat:")[1]
    await state.update_data(category=category)
    logger.info(f"[FSM] Категория выбрана: {category}")

    levels = await get_all_levels()
    await callback.message.answer(
        f"📚 Вы выбрали категорию: {category}\n\nТеперь выберите уровень сложности:",
        reply_markup=level_keyboard(levels)
    )

    await state.set_state(QuizState.LevelSelected)
    logger.info("[FSM] Состояние переключено на: LevelSelected")

@router.message(StateFilter(QuizState.LevelSelected))
async def level_selected(message: Message, state: FSMContext):
    level = message.text.lower().strip()
    data = await state.get_data()
    category = data.get("category")

    if not category:
        await message.answer("❌ Ошибка: категория не найдена. Начните сначала /start")
        return

    valid_levels = await get_all_levels()
    valid_level_names = [l.lower() for l in valid_levels]

    if level != "все уровни" and level not in valid_level_names:
        await message.answer(
            "⚠️ Уровень не распознан. Пожалуйста, выберите один из предложенных.\n"
            f"Доступные уровни: {', '.join(valid_levels)}"
        )
        return

    await state.update_data(level=level)
    await state.set_state(QuizState.AwaitingWordCount)

    # Получаем все слова и фильтруем по категории и уровню
    all_words = await get_all_words()
    filtered_words = [
        w for w in all_words
        if w['category'].lower() == category.lower() and (
                level == "все уровни" or (w['level'] and w['level'].lower() == level)
        )
    ]

    # Проверка на пустой результат
    if not filtered_words:
        await message.answer("⚠️ В этой категории и уровне нет слов. Попробуйте выбрать другую категорию или уровень.")
        return

    # Отправляем сообщение с количеством слов
    await message.answer(
        f"✅ Вы выбрали:\nКатегория: {category}\nУровень: {level}\nВсего слов: {len(filtered_words)}\n\n"
        "Сколько слов вы хотите пройти в этой тренировке? (например, 5, 10, 15)"
    )



    # await message.answer(
    #     f"✅ Вы выбрали:\nКатегория: {category}\nУровень: {level}\n\n"
    #     "Сколько слов вы хотите пройти в этой тренировке? (например, 5, 10, 15)"
    # )

@router.message(StateFilter(QuizState.AwaitingWordCount))
async def word_count_selected(message: Message, state: FSMContext):
    try:
        count = int(message.text.strip())
        if count <= 0 or count > 20:
            raise ValueError
    except ValueError:
        await message.answer("Введите число от 1 до 20.")
        return

    data = await state.get_data()
    category = data.get("category")
    level = data.get("level")

    await start_quiz(message, category, level, count, state)

async def start_quiz(message: Message, category: str, level: str | None, limit: int, state: FSMContext):
    words = await get_words_for_quiz(category, level, limit)
    if not words:
        await message.answer("❌ Нет слов по выбранной категории и уровню.")
        return

    await message.answer("✅ Начинаем викторину!")

    await state.set_state(QuizState.in_quiz)
    await state.update_data(words=words, score=0, index=0)

    current_word = words[0]
    question = current_word["word_esp"]

    options = [
        current_word["word_rus"],
        current_word.get("other_rus1"),
        current_word.get("other_rus2"),
        current_word.get("other_rus3"),
    ]
    options = [opt for opt in options if opt]
    shuffle(options)

    await message.answer(
        f"Как переводится: {question}?",
        reply_markup=answer_keyboard(options)
    )

@router.message(StateFilter(QuizState.in_quiz))
async def process_quiz_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    words = data.get("words", [])
    score = data.get("score", 0)
    index = data.get("index", 0)

    if index >= len(words):
        await message.answer(
            f"🏁 Тренировка окончена! Ваш результат: {score} правильных ответов из {len(words)}.\n\n"
            "🎉 Поздравляем! Чтобы начать новую тренировку, нажмите /start.",
            reply_markup=start_over_keyboard
        )
        await state.clear()
        return

    current_word = words[index]
    correct_answer = current_word["word_rus"]
    user_answer = message.text.strip().lower()

    if user_answer == correct_answer.lower():
        score += 1
        await message.answer("✅ Верно!")
    else:
        await message.answer(f"❌ Неверно! Правильный ответ: {correct_answer}")

    index += 1

    if index >= len(words):
        await message.answer(
            f"🏁 Тренировка окончена! Ваш результат: {score} правильных ответов из {len(words)}.\n\n"
            "🎉 Поздравляем! Чтобы начать новую тренировку, нажмите /start.",
            reply_markup=start_over_keyboard
        )
        await state.clear()
        return

    next_word = words[index]
    question = next_word["word_esp"]

    options = [
        next_word["word_rus"],
        next_word.get("other_rus1"),
        next_word.get("other_rus2"),
        next_word.get("other_rus3"),
    ]
    options = [opt for opt in options if opt]
    shuffle(options)

    await state.update_data(index=index, score=score)
    await message.answer(
        f"Как переводится: {question}?",
        reply_markup=answer_keyboard(options)
    )

@router.message(Command("cancel"))
async def cancel_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Действие отменено. Возвращаемся в начало ⤵️")
    await cmd_start(message, state)