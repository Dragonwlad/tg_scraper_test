import asyncio
import logging
import signal

from telegram_scraper.db.init_db import init_db
from telegram_scraper.scheduler.scheduler import start_scheduler

logger = logging.getLogger(__name__)


async def main():
    await init_db()
    stop_event = asyncio.Event()

    def handle_exit():
        logger.info("Остановка по сигналу...")
        stop_event.set()

    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, handle_exit)
    loop.add_signal_handler(signal.SIGTERM, handle_exit)

    start_scheduler()
    print("Scheduler started. Waiting for tasks...")
    await stop_event.wait()


if __name__ == '__main__':
    asyncio.run(main())
