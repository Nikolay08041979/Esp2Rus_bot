# --- Новый файл: bot/handlers/admin_handlers.py ---
import logging
import os
from aiogram import Router, Bot, F
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from datetime import datetime
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, BufferedInputFile
from core.config import ADMIN_IDS, DB
from core.file_utils import save_uploaded_csv, save_import_log
from db.models import (
    get_category_stats,
    get_level_stats,
    add_category,
    delete_category,
    add_level,
    delete_level,
    get_all_levels_text,
)
from db.importer import import_words_from_json
from core.converter import convert_csv_to_json
from bot.states.admin_states import AdminStates, AdminReportState
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


from analytics.reports.generate_admin_report_csv import generate_admin_report_csv
from analytics.reports.generate_user_report import generate_user_report
from analytics.reports.generate_admin_day_report import generate_admin_day_report
from analytics.reports.generate_cron_log_report import generate_cron_log_report



router = Router()

# --- Клавиатура админ-панели ---
def admin_menu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Статистика по категориям", callback_data="admin_stats")],
            [InlineKeyboardButton(text="📈 Статистика по уровням", callback_data="admin_stats_levels")],
            [InlineKeyboardButton(text="➕ Добавить категорию", callback_data="admin_add_category")],
            [InlineKeyboardButton(text="🗑 Удалить категорию", callback_data="admin_delete_category")],
            [InlineKeyboardButton(text="➕ Добавить уровень", callback_data="admin_add_level")],
            [InlineKeyboardButton(text="🗑 Удалить уровень", callback_data="admin_delete_level")],
            [InlineKeyboardButton(text="📅 Отчетность", callback_data="admin/report")]
        ]
    )

# --- Админский вход ---
@router.message(Command("admin"), StateFilter("*"))
async def admin_entry(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔ У вас нет прав администратора.")
        return

    await state.clear()

    help_text = (
        "🔧 Добро пожаловать в админ-панель!\n\n"
    )

    await message.answer(help_text, reply_markup=admin_menu_keyboard())



# --- Переход в меню отчётности по нажатию на кнопку "📅 Отчётность" (текстовое сообщение)
@router.message(F.text.lower().contains("отчетность"), StateFilter("*"))
async def redirect_to_report_menu(message: Message, state: FSMContext):
    await state.clear()
    await start_admin_report_menu(message, state)


# --- Команда /admin/report (вход в FSM меню)
@router.message(Command("admin/report"))
async def start_admin_report_menu(message: Message, state: FSMContext):
    print("✅ Вошли в admin/report")
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔ У вас нет прав администратора.")
        return

    await state.clear()
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📅 Отчет за день")],
        [KeyboardButton(text="🗓️ Отчет за месяц (CSV)")],
        [KeyboardButton(text="👤 Отчет по пользователю")]
    ], resize_keyboard=True)

    await message.answer("📊 Выберите тип отчета:", reply_markup=keyboard)
    await state.set_state(AdminReportState.choosing_mode)


# --- Блок повторного входа в FSM меню
@router.message(AdminReportState.choosing_mode, Command("admin/report"))
async def block_if_busy(message: Message, state: FSMContext):
    await message.answer("⚠️ Вы уже в меню отчетности. Завершите текущую операцию или нажмите /cancel.")

# --- Кнопка inline admin_menu: "📅 Отчетность"
@router.callback_query(F.data == "admin/report")
async def handle_admin_report_callback(callback: CallbackQuery, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📅 Отчет за день")],
        [KeyboardButton(text="🗓️ Отчет за месяц (CSV)")],
        [KeyboardButton(text="👤 Отчет по пользователю")]
    ], resize_keyboard=True)

    await callback.message.answer("📊 Выберите тип отчета:", reply_markup=keyboard)
    await state.set_state(AdminReportState.choosing_mode)


# --- Статистика по категориям ---
@router.callback_query(F.data == "admin_stats")
async def show_stats(callback: CallbackQuery):
    stats = await get_category_stats()
    lines = [f"{r['категория']}: {r['количество_слов']}" for r in stats]
    await callback.message.answer("📊 Кол-во слов по категориям:\n\n" + "\n".join(lines))

# --- Статистика по уровням ---
@router.callback_query(F.data == "admin_stats_levels")
async def show_level_stats(callback: CallbackQuery):
    stats = await get_level_stats()
    lines = [f"{r['уровень']}: {r['количество_слов']}" for r in stats]
    await callback.message.answer("📈 Кол-во слов по уровням:\n\n" + "\n".join(lines))

# --- Добавить категорию ---
@router.callback_query(F.data == "admin_add_category")
async def prompt_add_category(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("✏️ Введите название новой категории:")
    await state.set_state(AdminStates.awaiting_new_category)

@router.message(AdminStates.awaiting_new_category)
async def receive_new_category(message: Message, state: FSMContext):
    result = await add_category(message.text)
    await message.answer(result)
    await state.clear()

# --- Удалить категорию ---
@router.callback_query(F.data == "admin_delete_category")
async def prompt_delete_category(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🗑 Введите название категории для удаления:")
    await state.set_state(AdminStates.awaiting_delete_category)

@router.message(AdminStates.awaiting_delete_category)
async def receive_category_to_delete(message: Message, state: FSMContext):
    result = await delete_category(message.text)
    await message.answer(result)
    await state.clear()

# --- Добавить уровень ---
@router.callback_query(F.data == "admin_add_level")
async def prompt_add_level(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("✏️ Введите название нового уровня:")
    await state.set_state(AdminStates.awaiting_new_level)

@router.message(AdminStates.awaiting_new_level)
async def receive_new_level(message: Message, state: FSMContext):
    result = await add_level(message.text)
    await message.answer(result)
    await state.clear()

# --- Удалить уровень ---
@router.callback_query(F.data == "admin_delete_level")
async def prompt_delete_level(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🗑 Введите название уровня для удаления:")
    await state.set_state(AdminStates.awaiting_delete_level)

@router.message(AdminStates.awaiting_delete_level)
async def receive_level_to_delete(message: Message, state: FSMContext):
    result = await delete_level(message.text)
    await message.answer(result)
    await state.clear()

# --- Обработка загрузки CSV-файлов ---
@router.message(F.document)
async def handle_csv_upload(message: Message, bot: Bot, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔ У вас нет прав администратора.")
        return

    if not message.document.file_name.endswith(".csv"):
        await message.answer("⚠️ Пожалуйста, отправьте файл с расширением .csv")
        return

    # Сохраняем файл
    file = await bot.get_file(message.document.file_id)
    file_data = await bot.download_file(file.file_path)
    file_path = save_uploaded_csv(message.document.file_name, file_data.read())

    # Конвертация CSV → JSON
    json_path = file_path + ".json"
    convert_csv_to_json(file_path, json_path)

    # Импорт слов
    result = await import_words_from_json(json_path, DB)

    # Логирование загрузки
    log_path = save_import_log(result)

    # Ответ пользователю
    msg = (
        "✅ **Результаты загрузки файла:**\n\n"
        f"➕ Добавлено слов: **{result['added']}**\n"
        f"➖ Дубликаты: **{len(result['duplicates'])}**\n"
        f"⚠️ Ошибки: **{len(result['errors'])}**\n\n"
        f"📝 Лог: `{log_path}`"
    )
    await message.answer(msg, parse_mode="Markdown")

@router.message(AdminReportState.choosing_mode, F.text.lower().contains("отчет за день"))
async def request_day_report(message: Message, state: FSMContext):
    logging.info("🟢 Вызван хендлер request_day_report")
    await message.answer("📅 Введите дату для отчета в формате *дд.мм.гггг*", parse_mode="Markdown")
    await state.set_state(AdminReportState.enter_date)

@router.message(AdminReportState.enter_date)
async def handle_admin_report_date(message: Message, state: FSMContext):
    try:
        report_date = datetime.strptime(message.text.strip(), "%d.%m.%Y").date()
    except ValueError:
        await message.answer("❌ Неверный формат. Пример: *12.05.2025*", parse_mode="Markdown")
        return

    try:
        report = await generate_admin_day_report(report_date)
        await message.answer(report)
    except Exception as e:
        await message.answer(f"❌ Ошибка при формировании отчета: {e}")
    await state.clear()

@router.message(AdminReportState.choosing_mode, F.text.lower().contains("отчет за месяц"))
async def generate_month_csv(message: Message, state: FSMContext):
    path = await generate_admin_report_csv(days=30)
    if os.path.exists(path):
        doc = FSInputFile(path)  # ✅ Правильно обернули путь в FSInputFile
        await message.answer_document(doc, caption="📦 отчет за последний месяц")
    else:
        await message.answer("❌ Не удалось сформировать отчет.")
    await state.clear()


@router.message(AdminReportState.choosing_mode, F.text.lower().contains("отчет по пользователю"))
async def request_user_id(message: Message, state: FSMContext):
    await message.answer("Введите Telegram ID или username (например, 123456 или @user):")
    await state.set_state(AdminReportState.enter_user)

@router.message(AdminReportState.enter_user)
async def handle_user_report(message: Message, state: FSMContext):
    user_input = message.text.strip()

    try:
        report = await generate_user_report(user_input)  # передаём строку как есть
        await message.answer(report)
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
    await state.clear()

@router.message(F.text.startswith("/admin/report/log"))
async def handle_admin_log_report(message: Message):
    tg_id = message.from_user.id
    if tg_id not in ADMIN_IDS:
        await message.answer("⛔ У вас нет прав для выполнения этой команды.")
        return

    try:
        # Парсим количество дней (если указано)
        parts = message.text.strip().split("/")

        # Если указан конкретный N (например, /admin/report/log/7)
        if len(parts) == 4 and parts[3].isdigit():
            days = int(parts[3])
        else:
            days = 30  # по умолчанию

        csv_data = await generate_cron_log_report(days)

        if csv_data.startswith("❌"):
            await message.answer(csv_data)
            return

        # Отправляем CSV как файл
        output_file = BufferedInputFile(
            file=csv_data.encode("utf-8"),
            filename=f"log_report_last_{days}_days.csv"
        )

        await message.answer_document(
            document=output_file,
            caption=f"📄 Логи за последние {days} дней"
        )

    except Exception as e:
        await message.answer(f"❌ Ошибка при формировании отчета: {e}")

# --- DEBUG: выводим всё, что приходит в choosing_mode
@router.message(AdminReportState.choosing_mode)
async def debug_report_state(message: Message, state: FSMContext):
    current_state = await state.get_state()
    print(f"🛠 DEBUG — choosing_mode активен!")
    print(f"🔹 Получено сообщение: {message.text}")
    print(f"🔹 Текущее состояние: {current_state}")

    await message.answer("⚠️ Не удалось распознать команду в меню отчетности. Попробуйте снова или нажмите /cancel.")
