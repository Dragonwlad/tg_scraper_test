import asyncio
import logging

from datetime import datetime
from typing import List
from telethon.tl.types import Message

from telegram_scraper.config.settings import settings
from telegram_scraper.db.database import get_db_session
from telegram_scraper.db.models import TelegramPost
from telegram_scraper.telegram_client.client import TelegramService
from telegram_scraper.repositories import get_max_message_id_by_channel, bulk_save_new_messages

logger = logging.getLogger(__name__)


class MessageCollector:
    """
    Класс для сбора и сохранения сообщений из Telegram-каналов.
    """

    def __init__(self, tg_service: TelegramService, channels: List[int], message_limit: int = 50):
        """
        Инициализация MessageCollector.

        :param tg_service: Сервис для работы с Telegram API.
        :param channels: Список каналов для сбора сообщений.
        """
        self.tg_service: TelegramService = tg_service
        self.channels: list[int] = channels
        self.message_limit: int = message_limit

    async def collect_telegram_messages(self) -> None:
        """
        Основная функция для сбора сообщений.
        """
        logger.info('Запуск сбора сообщений.')
        tasks = [
            self._collect_messages_for_channel(channel_id) for channel_id in self.channels
        ]
        await asyncio.gather(*tasks, return_exceptions=True)

    async def _collect_messages_for_channel(self, channel_id: int) -> None:
        """
        Выполняет сбор сообщений для одного канала.
        """
        logger.info(f'Сбор сообщений для канала: {channel_id}')

        messages = await self._get_messages_from_channel(channel_id)
        new_messages = await self._filter_new_messages(messages, channel_id)
        await self._save_new_messages(new_messages)

    async def _get_messages_from_channel(self, channel_id: int) -> List[Message]:
        """
        Получает последние сообщения из канала.
        """
        messages = await self.tg_service.get_last_messages_from_channel(channel_id, self.message_limit)
        return messages

    async def _filter_new_messages(self, messages: List[Message], channel_id: int) -> List[TelegramPost]:
        """
        Проверяет, какие сообщения новые, и фильтрует уже сохранённые, основываясь на максимальном message_id в БД.
        """
        new_messages = []

        max_message_id = await get_max_message_id_by_channel(channel_id) or 0

        for msg in messages:
            if msg.message is None:
                continue

            if msg.id > max_message_id:
                new_messages.append(TelegramPost(
                    channel_id=str(channel_id),
                    message_id=msg.id,
                    published_at=msg.date,
                    text=msg.message,
                    views=msg.views,
                ))
        logger.info('На канале: {channel_id}, найдено {len_msg} новых сообщений'.format(
            channel_id=channel_id,
            len_msg=len(new_messages),
            )
        )
        return new_messages

    async def _save_new_messages(self, messages: List[TelegramPost]) -> None:
        """
        Сохраняет новые сообщения в базу данных.
        """
        if not messages:
            return

        saved_msg = await bulk_save_new_messages(messages)
        logger.info('Сохранено {saved_msg} новых сообщений в БД.'.format(saved_msg=saved_msg if saved_msg > 0 else 0))


async def run_collect_telegram_messages():
    """
    Обёртка для асинхронного вызова collect_telegram_messages.
    """
    async with TelegramService() as tg_service:
        collector = MessageCollector(tg_service, settings.telegram_channels)
        await collector.collect_telegram_messages()


if __name__ == '__main__':
    async def save_message_to_db(messages: list[Message]):
        message = messages[0]
        tg_post = TelegramPost(
            message_id=1,
            channel_id='123123123',
            published_at=datetime.now(),
            text='test',
            views=22,
        )

        async with get_db_session() as session:
            session.add(tg_post)
            await session.commit()


    async def main():
        async with TelegramService() as tg:
            messages = await tg.get_last_messages_from_channel(1124038902)
            await save_message_to_db(messages)


    asyncio.run(main())
