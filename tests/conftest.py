import asyncio

import pytest
from faker import Faker


@pytest.fixture
def fake():
    return Faker("pt_BR")


@pytest.fixture
def event_loop():
    yield asyncio.get_event_loop()


def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
