from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import random

from db.models import get_all_categories, get_all_levels, get_words_for_quiz
from bot.keyboards import category_keyboard, level_keyboard, quiz_options_keyboard, start_over_keyboard

# FSM состояния
class QuizState(StatesGroup):
    choosing_category = State()
    choosing_level = State()
    choosing_quantity = State()
    quiz_in_progress = State()

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    categories = await get_all_categories()
    await state.update_data(categories=categories)
    await message.answer(
        "Привет! 👋\nЯ помогу тебе выучить испанские слова.\n\nВыбери категорию:",
        reply_markup=category_keyboard(categories)
    )
    await state.set_state(QuizState.choosing_category)

@router.message(QuizState.choosing_category)
async def choose_category(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text not in data['categories']:
        await message.answer("Пожалуйста, выбери категорию из списка.")
        return
    await state.update_data(category=message.text)
    levels = await get_all_levels()
    await state.update_data(levels=levels)
    await message.answer(
        "Отлично! Теперь выбери уровень сложности:",
        reply_markup=level_keyboard(levels)
    )
    await state.set_state(QuizState.choosing_level)

@router.message(QuizState.choosing_level)
async def choose_level(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text not in data['levels'] and message.text.lower() != "все уровни":
        await message.answer("Пожалуйста, выбери уровень из списка.")
        return
    await state.update_data(level=message.text if message.text != "все уровни" else None)
    await message.answer(
        "Сколько слов ты хочешь пройти? (например, 5, 10, 15)",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(QuizState.choosing_quantity)

@router.message(QuizState.choosing_quantity)
async def choose_quantity(message: types.Message, state: FSMContext):
    try:
        count = int(message.text)
        if count < 1 or count > 20:
            raise ValueError()
    except ValueError:
        await message.answer("Введите число от 1 до 20.")
        return

    await state.update_data(quantity=count)
    data = await state.get_data()

    await message.answer(
        f"Начинаем тренировку!\n\nКатегория: {data['category']}\nУровень: {data['level'] or 'все уровни'}\nСлов: {data['quantity']}"
    )
    await state.set_state(QuizState.quiz_in_progress)

    words = await get_words_for_quiz(data['category'], data['level'], data['quantity'])
    if not words:
        await message.answer("Нет слов по выбранным параметрам. Попробуй другую категорию или уровень.")
        await state.clear()
        return

    random.shuffle(words)
    await state.update_data(words=words, correct=0, total=0)

    first = words[0]
    options = [first['word_rus'], first['other_rus1'], first['other_rus2'], first['other_rus3']]
    random.shuffle(options)

    keyboard = quiz_options_keyboard(options)
    await message.answer(
        f"Как переводится: *{first['word_esp']}*?",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

@router.message(QuizState.quiz_in_progress)
async def handle_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    total = data.get('total', 0)
    correct = data.get('correct', 0)
    words = data.get('words', [])

    current = words[total]
    right_answer = current['word_rus']

    if message.text.strip().lower() == "пропустить":
        await message.answer(f"ℹ️ Пропущено. Правильный ответ: {right_answer}")
    elif message.text.strip().lower() == right_answer.strip().lower():
        correct += 1
        await message.answer("✅ Верно!")
    else:
        await message.answer(f"❌ Неверно. Правильный ответ: {right_answer}")

    total += 1
    if total >= len(words):
        percent = round(correct / total * 100)
        await message.answer(
            f"🏁 Викторина завершена!\nПравильных ответов: {correct} из {total} ({percent}%)",
            reply_markup=start_over_keyboard
        )
        await state.clear()
        return

    await state.update_data(total=total, correct=correct)

    next_word = words[total]
    options = [next_word['word_rus'], next_word['other_rus1'], next_word['other_rus2'], next_word['other_rus3']]
    random.shuffle(options)

    keyboard = quiz_options_keyboard(options)
    await message.answer(
        f"Как переводится: *{next_word['word_esp']}*?",
        parse_mode="Markdown",
        reply_markup=keyboard
    )