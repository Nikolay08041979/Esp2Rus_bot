
# 🔁 Ежедневная синхронизация всех клиентов (OFFLINE режим)
import asyncio
from analytics.metrics.sync_core import sync_client_analytics_all

async def main():
    await sync_client_analytics_all()

if __name__ == "__main__":
    asyncio.run(main())
