import asyncio

from sqlalchemy import text
from telegram_scraper.db.database import get_db_session


async def init_db():

    tg_message_table = r"""

    CREATE TABLE IF NOT EXISTS telegram_posts (
      id SERIAL PRIMARY KEY,
      channel_id TEXT NOT NULL,
      message_id BIGINT NOT NULL,
      published_at TIMESTAMP NOT NULL,
      text TEXT,
      views INTEGER,
      collected_at TIMESTAMP DEFAULT NOW()
    );
    """

    async with get_db_session() as session:
        await session.execute(text(tg_message_table))
        await session.commit()


if __name__ == '__main__':
    asyncio.run(init_db())
