# --- Новый файл: bot/handlers/admin_handlers.py ---

from aiogram import Router, Bot, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

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
from bot.states.admin_states import AdminStates

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
        ]
    )

# --- Админский вход ---
@router.message(Command("admin"), StateFilter("*"))
async def admin_entry(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔ У вас нет прав администратора.")
        return

    await state.clear()
    await message.answer("🔧 Добро пожаловать в админ-панель:", reply_markup=admin_menu_keyboard())


# @router.message(Command("admin"))
# async def admin_entry(message: Message):
#     if message.from_user.id not in ADMIN_IDS:
#         await message.answer("⛔ У вас нет прав администратора.")
#         return
#     await message.answer("🔧 Добро пожаловать в админ-панель:", reply_markup=admin_menu_keyboard())

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