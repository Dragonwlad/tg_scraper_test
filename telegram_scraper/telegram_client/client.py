import logging

from telethon import TelegramClient
from telethon.errors import FloodWaitError, RPCError
from telethon.tl.types import Message, PeerChannel

from telegram_scraper.config.settings import settings, Settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ChanelNotFound(Exception):
    """Канал не найден."""


class TelegramService:
    """
    Класс для подключения и работы с Telegram через Telethon.
    """

    def __init__(self, proj_settings: Settings = settings) -> None:
        self.phone_number: str = proj_settings.phone_number
        self.client: TelegramClient = TelegramClient(
            proj_settings.session_file_path,
            proj_settings.api_id,
            proj_settings.api_hash,
        )

    async def __aenter__(self) -> 'TelegramService':
        logger.debug('Подключение к Telegram')
        await self.client.connect()
        if not await self.client.is_user_authorized():
            await self._authorize_user()
        logger.debug('Подключение к Telegram успешно')
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        logger.debug('Отключение от Telegram')
        await self.disconnect()

    async def disconnect(self) -> None:
        """
        Отключение от Telegram API.
        """
        await self.client.disconnect()
        logger.info('Отключение от Telegram')

    async def get_last_messages_from_channel(self, channel_id: int, message_limit: int) -> list[Message]:
        """
        Получение последних сообщений из канала по его ID.
        """
        try:
            channel = await self.client.get_entity(PeerChannel(channel_id))
            messages: list[Message] = await self.client.get_messages(channel, limit=message_limit)
            logger.info('Получено {len_msg} сообщений из канала {channel_id}'.format(
                len_msg=len(messages),
                channel_id=channel_id,
                )
            )
            return messages
        except ValueError as error:
            logger.warning(
                'Ошибка при получении сообщений из канала {channel_id}. Возможно, его не существует. {error}'.format(
                    channel_id=channel_id,
                    error=error,
                    )
            )
            raise error
        except (FloodWaitError, RPCError) as error:
            logger.exception('Ошибка при получении сообщений из канала {channel_id}: {error}'.format(
                channel_id=channel_id,
                error=error,
                )
            )
        except Exception as error:
            logger.warning(
                'Неизвестная ошибка при запросе канала/сообщений. {error}'.format(
                    error=error,
                    )
            )
            raise error

    async def _authorize_user(self) -> None:
        """
        Авторизует пользователя, если требуется.
        """
        logger.info('Авторизация пользователя...')
        await self.client.send_code_request(self.phone_number)
        code = input('Введите код из Telegram: ')
        await self.client.sign_in(self.phone_number, code)
        logger.info('Авторизация успешно завершена.')
