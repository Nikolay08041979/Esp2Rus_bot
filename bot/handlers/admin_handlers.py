from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton

from core.config import ADMIN_IDS, DB
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

import os

router = Router()

def admin_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Статистика по категориям", callback_data="admin_stats")],
        [InlineKeyboardButton(text="📈 Статистика по уровням", callback_data="admin_stats_levels")],
        [InlineKeyboardButton(text="➕ Добавить категорию", callback_data="admin_add_category")],
        [InlineKeyboardButton(text="🗑 Удалить категорию", callback_data="admin_delete_category")],
        [InlineKeyboardButton(text="📋 Посмотреть уровни", callback_data="admin_list_levels")],
        [InlineKeyboardButton(text="➕ Добавить уровень", callback_data="admin_add_level")],
        [InlineKeyboardButton(text="🗑 Удалить уровень", callback_data="admin_delete_level")],
    ])

@router.message(Command("admin"))
@router.message(F.text.lower() == "/admin")
async def admin_entry(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔ У вас нет прав администратора.")
        return
    await message.answer("🔧 Добро пожаловать в админ-панель:", reply_markup=admin_menu_keyboard())

@router.message(F.document)
async def handle_csv_upload(message: Message, bot: Bot, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔ У вас нет прав администратора.")
        return

    if not message.document.file_name.endswith(".csv"):
        await message.answer("⚠️ Пожалуйста, отправьте файл с расширением .csv")
        return

    os.makedirs("data/uploads", exist_ok=True)
    file_path = f"data/uploads/{message.document.file_name}"
    file = await bot.get_file(message.document.file_id)
    await bot.download_file(file.file_path, destination=file_path)

    json_path = "data/words.json"
    convert_csv_to_json(file_path, json_path)
    result = await import_words_from_json(json_path, DB)

    await message.answer(
        f"✅ Файл обработан.\n"
        f"Добавлено: {result['added']}\n"
        f"Пропущено (дубликаты): {len(result['duplicates'])}\n"
        f"Ошибки: {len(result['errors'])}"
    )

@router.callback_query(F.data == "admin_stats")
async def show_stats(callback: CallbackQuery):
    stats = await get_category_stats()
    lines = [f"{r['категория']}: {r['количество_слов']}" for r in stats]
    await callback.message.answer("📊 Кол-во слов по категориям:" + "\n".join(lines))

@router.callback_query(F.data == "admin_stats_levels")
async def show_level_stats(callback: CallbackQuery):
    stats = await get_level_stats()
    lines = [f"{r['уровень']}: {r['количество_слов']}" for r in stats]
    await callback.message.answer("📈 Кол-во слов по уровням:" + "\n".join(lines))

@router.callback_query(F.data == "admin_add_category")
async def prompt_add_category(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите название новой категории:")
    await state.set_state("awaiting_new_category")

@router.message(F.text, state="awaiting_new_category")
async def receive_new_category(message: Message, state: FSMContext):
    result = await add_category(message.text)
    await message.answer(result)
    await state.clear()

@router.callback_query(F.data == "admin_delete_category")
async def prompt_delete_category(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите название категории, которую хотите удалить:")
    await state.set_state("awaiting_delete_category")

@router.message(F.text, state="awaiting_delete_category")
async def receive_category_to_delete(message: Message, state: FSMContext):
    result = await delete_category(message.text)
    await message.answer(result)
    await state.clear()

@router.callback_query(F.data == "admin_add_level")
async def prompt_add_level(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите название нового уровня:")
    await state.set_state("awaiting_new_level")

@router.message(F.text, state="awaiting_new_level")
async def receive_new_level(message: Message, state: FSMContext):
    result = await add_level(message.text)
    await message.answer(result)
    await state.clear()

@router.callback_query(F.data == "admin_delete_level")
async def prompt_delete_level(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите название уровня, который нужно удалить:")
    await state.set_state("awaiting_delete_level")

@router.message(F.text, state="awaiting_delete_level")
async def receive_level_to_delete(message: Message, state: FSMContext):
    result = await delete_level(message.text)
    await message.answer(result)
    await state.clear()

@router.callback_query(F.data == "admin_list_levels")
async def list_all_levels(callback: CallbackQuery):
    levels = await get_all_levels_text()
    await callback.message.answer("📋 Список уровней:" + "\n".join(levels))