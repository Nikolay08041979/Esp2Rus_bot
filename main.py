from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

import asyncio
import logging

from core.config import BOT_TOKEN
from bot.handlers.user_handlers import router as user_router
from bot.handlers.admin_handlers import router as admin_router


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(user_router)
    dp.include_router(admin_router)

    # Команды бота
    await bot.set_my_commands([
        BotCommand(command="start", description="Начать тренировку"),
        BotCommand(command="cancel", description="Остановить текущую операцию"),
        BotCommand(command="help", description="Помощь по боту")
    ])

    print("🤖 Бот запущен.")
    await dp.start_polling(bot)

    print("BOT_TOKEN =", BOT_TOKEN, type(BOT_TOKEN))


if __name__ == "__main__":
    asyncio.run(main())