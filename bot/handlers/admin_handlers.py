from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from core.config import ADMIN_IDS
from db.models import get_category_stats, add_category, delete_category
from bot.keyboards import admin_menu_keyboard


router = Router()

# Inline-клавиатура для админ-команд
def admin_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Статистика по категориям", callback_data="admin_stats")],
        [InlineKeyboardButton(text="📊 Статистика по уровням", callback_data="admin_stats_levels")],
        [InlineKeyboardButton(text="➕ Добавить категорию", callback_data="admin_add_category")],
        [InlineKeyboardButton(text="🗑 Удалить категорию", callback_data="admin_delete_category")],
        [InlineKeyboardButton(text="📘 Посмотреть уровни", callback_data="admin_list_levels")],
        [InlineKeyboardButton(text="➕ Добавить уровень", callback_data="admin_add_level")],
        [InlineKeyboardButton(text="🗑 Удалить уровень", callback_data="admin_delete_level")]
    ])

@router.message(F.text == "/admin")
async def admin_entry(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔ У вас нет прав администратора.")
        return
    await message.answer("🔧 Админ-панель:", reply_markup=admin_menu_keyboard())

@router.callback_query(F.data == "admin_stats")
async def show_stats(callback: types.CallbackQuery):
    stats = await get_category_stats()
    text = "\n".join(f"📚 {row['категория']}: {row['количество_слов']}" for row in stats)
    await callback.message.answer(f"📊 Кол-во слов по категориям:\n\n{text}", reply_markup=admin_menu_keyboard())

# В перспективе:
# - Реализовать команды "admin_add_category", "admin_delete_category"

from aiogram.fsm.state import State, StatesGroup

class AdminFSM(StatesGroup):
    waiting_for_new_level = State()
    waiting_for_level_to_delete = State()
    waiting_for_new_category = State()
    waiting_for_category_to_delete = State()

@router.callback_query(F.data == "admin_add_category")
async def prompt_add_category(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("✏️ Введите название новой категории (например: животные, транспорт):\n⚠️ Только в нижнем регистре!")
    await state.set_state(AdminFSM.waiting_for_new_category)

@router.message(AdminFSM.waiting_for_new_category)
async def add_category_handler(message: types.Message, state: FSMContext):
    name = message.text.strip().lower()
    result = await add_category(name)
    await message.answer(result)
    await state.clear()
    await message.answer("🔧 Что дальше?", reply_markup=admin_menu_keyboard())

@router.callback_query(F.data == "admin_delete_category")
async def prompt_delete_category(callback: types.CallbackQuery, state: FSMContext):
    from db.models import get_all_categories
    categories = await get_all_categories()
    cat_list = "\n".join(f"🔹 {c}" for c in categories)
    await callback.message.answer(f"❗ Введите название категории, которую нужно удалить:\n\n📚 Доступные категории:\n{cat_list}")
    await state.set_state(AdminFSM.waiting_for_category_to_delete)

@router.message(AdminFSM.waiting_for_category_to_delete)
async def delete_category_handler(message: types.Message, state: FSMContext):
    name = message.text.strip().lower()
    result = await delete_category(name)
    await message.answer(result)
    await state.clear()
    await message.answer("🔧 Что дальше?", reply_markup=admin_menu_keyboard())

@router.callback_query(F.data == "admin_list_levels")
async def list_levels(callback: types.CallbackQuery):
    from db.models import get_all_levels_text
    levels = await get_all_levels_text()
    text = "\n".join(f"🔹 {lev}" for lev in levels)
    await callback.message.answer(f"📘 Список уровней:\n\n{text}", reply_markup=admin_menu_keyboard())

@router.callback_query(F.data == "admin_add_level")
async def prompt_add_level(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("✏️ Введите название нового уровня (например: начальный, средний):\n⚠️ Только прилагательное в нижнем регистре!")
    await state.set_state(AdminFSM.waiting_for_new_level)

@router.message(AdminFSM.waiting_for_new_level)
async def add_level_handler(message: types.Message, state: FSMContext):
    from db.models import add_level
    name = message.text.strip().lower()
    result = await add_level(name)
    await message.answer(result)
    await state.clear()
    await message.answer("🔧 Что дальше?", reply_markup=admin_menu_keyboard())

@router.callback_query(F.data == "admin_delete_level")
async def prompt_delete_level(callback: types.CallbackQuery, state: FSMContext):
    from db.models import get_all_levels_text
    levels = await get_all_levels_text()
    lev_list = "\n".join(f"🔹 {l}" for l in levels)
    await callback.message.answer(f"❗ Введите уровень, который нужно удалить:\n\n📘 Доступные уровни:\n{lev_list}")
    await state.set_state(AdminFSM.waiting_for_level_to_delete)

@router.message(AdminFSM.waiting_for_level_to_delete)
async def delete_level_handler(message: types.Message, state: FSMContext):
    from db.models import delete_level
    name = message.text.strip().lower()
    result = await delete_level(name)
    await message.answer(result)
    await state.clear()
    await message.answer("🔧 Что дальше?", reply_markup=admin_menu_keyboard())

@router.callback_query(F.data == "admin_stats_levels")
async def show_level_stats(callback: types.CallbackQuery):
    from db.models import get_level_stats
    stats = await get_level_stats()
    text = "\n".join(f"📘 {row['уровень']}: {row['количество_слов']}" for row in stats)
    await callback.message.answer(f"📊 Кол-во слов по уровням:\n\n{text}", reply_markup=admin_menu_keyboard())