from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram_scraper.scheduler.jobs import register_jobs
import logging

logger = logging.getLogger(__name__)


def get_scheduler() -> AsyncIOScheduler:
    """
    Инициализирует и настраивает планировщик APScheduler.
    """
    scheduler = AsyncIOScheduler(timezone="UTC")
    register_jobs(scheduler)
    return scheduler


def start_scheduler() -> None:
    """
    Запускает планировщик APScheduler.
    """
    scheduler = get_scheduler()
    scheduler.start()
    logger.info("Планировщик задач запущен.")
