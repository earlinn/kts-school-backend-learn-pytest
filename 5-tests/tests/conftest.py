import datetime
import functools

from dateutil import tz
from freezegun import freeze_time
from gino import GinoEngine
import pytest

from blog_app import settings
from blog_app.user.models import Session
from tests.fixtures import *

settings.config = settings.get_config(
    settings.BASE_DIR / "config" / "test.yaml"
)

from blog_app.web.app import create_app

DEFAULT_TIME = datetime.datetime(2020, 2, 15, 0, tzinfo=tz.UTC)


# Фикстура aiohttp-приложения
@pytest.fixture
def app():
    return create_app()


# Фикстура клиента, который ходит в наше приложение
@pytest.fixture
async def cli(aiohttp_client, app):
    client = await aiohttp_client(app)
    yield client


# Фикстура транзакции с откатом всех изменений после теста
@pytest.fixture(autouse=True)
async def db_transaction(cli):

    db = cli.app["store"].db
    real_acquire = GinoEngine.acquire

    async with db.acquire() as conn:

        class _AcquireContext:
            __slots__ = ["_acquire", "_conn"]

            def __init__(self, acquire):
                self._acquire = acquire

            async def __aenter__(self):
                return conn

            async def __aexit__(self, exc_type, exc_val, exc_tb):
                pass

            def __await__(self):
                return conn

        def acquire(
            self, *, timeout=None, reuse=False, lazy=False, reusable=True
        ):
            return _AcquireContext(
                functools.partial(self._acquire, timeout, reuse, lazy, reusable)
            )

        GinoEngine.acquire = acquire
        transaction = await conn.transaction()
        yield
        await transaction.rollback()
        GinoEngine.acquire = real_acquire


# Мокаем дефолтное время с помощью библиотеки freezegun
@pytest.fixture
def freeze_t():
    freezer = freeze_time(DEFAULT_TIME)
    freezer.start()
    yield DEFAULT_TIME
    freezer.stop()


# Фикстура, возвращающая авторизованного клиента
class authenticate:
    def __init__(self, cli, user) -> None:
        self.cli = cli
        self.user = user

    async def __aenter__(self):
        session = await Session.generate(self.user.id)
        self.cli.session._default_headers["Authorization"] = (
            f"Bearer {session.key}"
        )

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.cli.session._default_headers.pop("Authorization")
