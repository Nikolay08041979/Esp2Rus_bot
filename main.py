import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from bot.handlers.user_handlers import router as user_router
from bot.handlers.admin_handlers import router as admin_router

# ✅ Загрузка переменных окружения
load_dotenv()

# ✅ Выбор токена по ENV_MODE
env = os.getenv("ENV_MODE", "dev")
token = os.getenv("BOT_TOKEN_PROD") if env == "prod" else os.getenv("BOT_TOKEN_DEV")

# ✅ Логирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)
logger.info(f"Запуск бота в режиме: {env}")

async def main():
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(user_router)
    dp.include_router(admin_router)

    await bot.set_my_commands([
        BotCommand(command="start", description="Начать тренировку"),
        BotCommand(command="cancel", description="Остановить текущую операцию"),
        BotCommand(command="help", description="Помощь по боту")
    ])

    logger.info("🤖 Бот успешно запущен и готов к приёму обновлений.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())