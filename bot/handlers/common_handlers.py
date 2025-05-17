from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.handlers.user_handlers import show_start_menu  # если используется общее стартовое меню

router = Router()

@router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Действие отменено. Возвращаемся в начало.")
    await show_start_menu(message, state)
