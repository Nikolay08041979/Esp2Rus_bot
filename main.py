import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from core.config import BOT_TOKEN
from bot.handlers.user_handlers import router as user_router
from bot.handlers.admin_handlers import router as admin_router

from bot.handlers.common_handlers import router as common_router


# ✅ Глобальная настройка логгирования (в начале файла)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)
logger.info("Бот запускается...")

async def main():
    # ✅ Создание бота и диспетчера
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=MemoryStorage())

    # ✅ Регистрация роутеров
    dp.include_router(common_router)
    dp.include_router(admin_router)
    dp.include_router(user_router)

    # ✅ Установка команд
    await bot.set_my_commands([
        BotCommand(command="start", description="Начать тренировку"),
        BotCommand(command="cancel", description="Остановить текущую операцию"),
        BotCommand(command="help", description="Помощь по боту"),
        BotCommand(command="report", description="Отчет о ваших достижениях"),
    ])

    logger.info("🤖 Бот успешно запущен и готов к приёму обновлений.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())