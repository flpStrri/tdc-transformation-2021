from unittest.mock import MagicMock

from pytest import fixture

from application.foo_service import FooService
from infrastructure.foo_repository import FooRepository


class FooServiceFixtures:
    @fixture
    def foo_repository(self):
        return MagicMock(spec=FooRepository)

    @fixture
    def service(self, foo_repository):
        return FooService(foo_repository=foo_repository)
