from sqlalchemy import Column, Integer, BigInteger, Text, TIMESTAMP, func, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TelegramPost(Base):
    """
    ORM-модель для хранения сообщений Telegram-каналов.
    """
    __tablename__ = 'telegram_posts'
    __table_args__ = (UniqueConstraint('channel_id', 'message_id', name='uq_channel_message'),)

    id: int = Column(Integer, primary_key=True, index=True)
    channel_id: str = Column(Text, nullable=False)
    message_id: int = Column(BigInteger, nullable=False)
    published_at: TIMESTAMP = Column(TIMESTAMP, nullable=False)
    text: str | None = Column(Text, nullable=True)
    views: int | None = Column(Integer, nullable=True)
    collected_at: TIMESTAMP = Column(TIMESTAMP, server_default=func.now())

    def __repr__(self) -> str:
        return f"<TelegramPost(channel_id='{self.channel_id}', message_id={self.message_id})>"
