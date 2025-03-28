import datetime
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from telegram_scraper.collector import run_collect_telegram_messages

logger = logging.getLogger(__name__)


def register_jobs(scheduler: AsyncIOScheduler) -> None:
    """
    Регистрирует задачи в планировщике.
    """
    scheduler.add_job(
        run_collect_telegram_messages,
        IntervalTrigger(hours=1),  # каждый час
        id='collect_telegram_messages_id',
        name="collect_telegram_messages",
        next_run_time=datetime.datetime.now(datetime.timezone.utc),
        replace_existing=True,
    )

    logger.info("Задача 'collect_telegram_messages' добавлена в планировщик.")
