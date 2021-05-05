from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://todos:todos@127.0.0.1:5432/todos"
metadata = MetaData()

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

ASYNC_SESSION = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
session = ASYNC_SESSION()
