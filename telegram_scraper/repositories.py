import logging

from sqlalchemy import select, func
from telegram_scraper.db.database import get_db_session
from telegram_scraper.db.models import TelegramPost


logger = logging.getLogger(__name__)


async def get_max_message_id_by_channel(channel_id: int) -> int | None:
    """
    Получает максимальный message_id для канала из базы данных.
    """
    logger.debug('Получение последнего сообщения с канала: {channel_id}'.format(channel_id=channel_id))
    async with get_db_session() as session:
        stmt = (
            select(func.max(TelegramPost.message_id))
            .where(TelegramPost.channel_id == str(channel_id))
        )
        result = await session.execute(stmt)
        logger.debug('Id последнего сообщен')
        max_message_id = result.scalar_one_or_none()

    return max_message_id


async def bulk_save_new_messages(messages: list[TelegramPost]):
    """
    Сохраняет множество сообщений в БД.
    """
    async with get_db_session() as session:
        message_dicts = [
            {
                'channel_id': post.channel_id,
                'message_id': post.message_id,
                'published_at': post.published_at.replace(tzinfo=None),
                'text': post.text,
                'views': post.views,
            }
            for post in messages
        ]
        result = await session.execute(
            TelegramPost.__table__.insert(),
            message_dicts,
        )
        await session.commit()

        row_count = result.rowcount if result else 0
    return row_count
