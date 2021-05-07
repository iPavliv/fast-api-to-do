from pydantic import BaseSettings

DB_URL = "127.0.0.1:5432"
DEV_DB_NAME = "todos"
TEST_DB_NAME = "test_todos"


class DevSettings(BaseSettings):
    database_url: str = f"postgresql+asyncpg://todos:todos@{DB_URL}/{DEV_DB_NAME}"
    isolation_level: str = "AUTOCOMMIT"


class TestSettings(BaseSettings):
    database_url: str = f"postgresql+asyncpg://todos:todos@{DB_URL}/{TEST_DB_NAME}"
    isolation_level: str = "READ_COMMITTED"


settings = {
    "dev": DevSettings,
    "test": TestSettings,
    "default": DevSettings,
}
