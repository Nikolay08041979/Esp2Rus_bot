# 📄 db/create_all.py

from db.create.archive.create_cron_events import create_cron_events_table
import asyncio

async def main():
    await create_cron_events_table()

if __name__ == "__main__":
    asyncio.run(main())
