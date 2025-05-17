import pprint
from datetime import datetime
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from bot.keyboards import category_keyboard, level_keyboard, answer_keyboard, start_over_keyboard
from bot.states import QuizState
from db.models import get_all_categories, get_all_levels, get_words_for_quiz, get_all_words, get_personalized_words
from random import shuffle
import logging
from analytics.analytics import log_client_activity
from analytics.metrics.get_level_id_word import get_level_id_word
from db.utils.client_lifecycle import ensure_client_registered
from analytics.reports.user_report import generate_user_report




logger = logging.getLogger(__name__)
router = Router()


# 🔁 Универсальный стартовый экран
async def show_start_menu(message: Message, state: FSMContext):
    await state.clear()
    categories = await get_all_categories()
    keyboard = category_keyboard(categories)
    await message.answer("👋 Привет! Пожалуйста, выбери категорию слов:", reply_markup=keyboard)


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await ensure_client_registered(message.from_user)
    await show_start_menu(message, state)


@router.message(Command("cancel"), flags={"allow_fsm": True})
async def cancel_command(message: Message, state: FSMContext):
    await message.answer("❌ Действие отменено. Возвращаемся в начало ⤵️")
    await show_start_menu(message, state)

@router.message(Command("report"))
async def handle_user_report(message: Message):
    report = await generate_user_report(message.from_user.id)
    await message.answer(report)


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
    if level == "все уровни":
        level = None  # используем None для универсальной фильтрации в SQL и Python

    data = await state.get_data()
    category = data.get("category")

    if not category:
        await message.answer("❌ Ошибка: категория не найдена. Начните сначала /start")
        return

    valid_levels = await get_all_levels()
    valid_level_names = [l.lower() for l in valid_levels]

    if level is not None and level not in valid_level_names:
        await message.answer(
            "⚠️ Уровень не распознан. Пожалуйста, выберите один из предложенных.\n"
            f"Доступные уровни: {', '.join(valid_levels)}"
        )
        return

    await state.update_data(level=level)
    await state.set_state(QuizState.AwaitingWordCount)

    all_words = await get_all_words()
    filtered_words = [
        w for w in all_words
        if w['category'].lower() == category.lower() and (
            level is None or (w['level'] and w['level'].lower() == level)
        )
    ]

    if not filtered_words:
        await message.answer("⚠️ В этой категории и уровне нет слов. Попробуйте выбрать другую категорию или уровень.")
        return

    # форматируем вывод уровня
    level_display = "все уровни" if level is None else level

    await message.answer(
        f"✅ Вы выбрали:\nКатегория: {category}\nУровень: {level_display}\nВсего слов: {len(filtered_words)}\n\n"
        "Сколько слов вы хотите пройти в этой тренировке? (например, 5, 10, 15)"
    )


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

   # await start_quiz(message, category, level, count, state)
    words = await get_personalized_words(message.from_user.id, category, level, count)

    print(f"[DEBUG word_count_selected] words returned: {len(words)}")

    if not words:
        level_display = "все уровни" if level is None else level
        if level_display == "все уровни":
            await message.answer(f"✅ Вы изучили все слова категории <b>{category}</b>. Выберите другую категорию.",
                                 parse_mode="HTML")
        else:
            await message.answer(
                f"✅ Вы изучили все слова уровня <b>{level_display}</b>. Выберите другой уровень или категорию.",
                parse_mode="HTML")
        return

    if len(words) < count:
        await message.answer(
            f"⚠️ Найдено только {len(words)} слов по выбранным параметрам. "
            "Начинаем тренировку с ними."
        )

    await start_quiz(message, words, state)

async def start_quiz(message: Message, words: list[dict], state: FSMContext):

    print(f"[DEBUG word_count_selected] words returned: {len(words)}")
    data = await state.get_data()
    category = data.get("category")
    level = data.get("level")
    level_display = "все уровни" if level is None else level

    if not words:
        if level_display == "все уровни":
            await message.answer(f"✅ Вы изучили все слова категории <b>{category}</b>. Выберите другую категорию.",
                                 parse_mode="HTML")
        else:
            await message.answer(
                f"✅ Вы изучили все слова уровня <b>{level_display}</b>. Выберите другой уровень или категорию.",
                parse_mode="HTML")
        return

    await message.answer("✅ Начинаем викторину!")

    await state.set_state(QuizState.in_quiz)

    await state.update_data(words=words, score=0, index=0, time_start=datetime.now().time())

    current_word = words[0]
    question = current_word["word_src"]

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
    # Получаем текущее состояние викторины из FSM
    data = await state.get_data()
    words = data.get("words", [])
    score = data.get("score", 0)
    index = data.get("index", 0)
    level = data.get("level", "все уровни")
    pprint.pp(data)

    logger.info(f"[QUIZ] Проверка завершения: index={index}, len(words)={len(words)}")
    # Проверка завершения викторины (>= — защита от сбоев/переполнения индекса)
    if index >= len(words):
        logger.warning(f"[QUIZ] Index {index} >= len(words)={len(words)} — викторина завершена, повтор.")
        result_text = (
            f"Тренировка окончена! Ваш результат: {int(100 * (score / len(words)))}% \n"
            f"({score} правильных ответов из {len(words)}).\n\n"
        )
        result_text += "🎉 Поздравляем!" if score == len(words) else "🎯 Ты почти у цели!"

        result_text += "Чтобы начать новую тренировку, нажмите /start."

        await message.answer(result_text, reply_markup=start_over_keyboard)

        # Защита: если уровень не указан, трактуем как "все уровни"
        level_display = "все уровни" if level is None else level

        level_id_word = await get_level_id_word(level_display)

        score_quiz = round(score / len(words), 2)

        time_finish = datetime.now().time()  # локальное время окончания
        time_start = data.get("time_start", time_finish)  # старт уже сохранён в FSM

        # Записываем результат в БД
        await log_client_activity(time_start, time_finish,{
            "tg_id": message.from_user.id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "language_code": message.from_user.language_code,
            "score_quiz": score_quiz,
            "words_correct_quiz": int(score),
            "words_incorrect_quiz": len(words) - int(score),
            "level_id_word": level_id_word,
            "words": words
        })

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
    await state.update_data(index=index, score=score)

    next_word = words[index] if index < len(words) else None

    if next_word:
        options = [
            next_word["word_rus"],
            next_word.get("other_rus1"),
            next_word.get("other_rus2"),
            next_word.get("other_rus3"),
        ]
        options = [opt for opt in options if opt]
        shuffle(options)

        await message.answer(
            f"Как переводится: {next_word['word_src']}?",
            reply_markup=answer_keyboard(options)
        )
    else:
        logger.info(f"[QUIZ] Завершаем викторину сразу после последнего вопроса. index={index}")
        return await process_quiz_answer(message, state)

