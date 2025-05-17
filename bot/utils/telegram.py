from aiogram import Bot
from aiogram.types import FSInputFile
from core.config import BOT_TOKEN

# Используем основной токен (или можно передать бот извне)
bot = Bot(token=BOT_TOKEN)

async def send_report_to_user(tg_id: int, message_text: str):
    try:
        await bot.send_message(chat_id=tg_id, text=message_text)
        print(f"[TG] Отчёт успешно отправлен пользователю {tg_id}")
    except Exception as e:
        print(f"[TG ERROR] Не удалось отправить отчёт пользователю {tg_id}: {e}")

async def send_report_to_admin(admin_id: int, message_text: str, file_path: str = None):
    try:
        await bot.send_message(chat_id=admin_id, text=message_text)

        if file_path:
            file = FSInputFile(file_path)
            await bot.send_document(chat_id=admin_id, document=file)

        print(f"[TG] Отчёт успешно отправлен администратору {admin_id}")
    except Exception as e:
        print(f"[TG ERROR] Не удалось отправить отчёт администратору {admin_id}: {e}")
