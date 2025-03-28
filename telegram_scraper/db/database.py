import logging
from contextlib import asynccontextmanager
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from telegram_scraper.config.settings import settings


logger = logging.getLogger(__name__)

engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_db_session() -> AsyncSession:
    session: AsyncSession = async_session()
    try:
        yield session
    except SQLAlchemyError:
        await session.rollback()
        raise
    except Exception as error:
        logger.error('Ошибка подключения к БД: {error}'.format(error=error))
    finally:
        await session.close()
