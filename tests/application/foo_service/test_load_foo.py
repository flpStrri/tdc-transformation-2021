import pytest
from aiodynamo.errors import ItemNotFound

from domain.foo import Foo
from tests.application.foo_service.foo_service_fixtures import FooServiceFixtures

pytestmark = pytest.mark.asyncio


class TestLoadFoo(FooServiceFixtures):
    async def test_should_return_repository_foo_given_no_failure(self, service, foo_repository):
        foo_repository.load_foo.return_value = Foo(identifier="bar", title="Bar")

        assert Foo(identifier="bar", title="Bar") == await service.load_foo("bar")

    async def test_should_raise_given_repository_failure(self, service, foo_repository):
        foo_repository.load_foo.side_effect = ItemNotFound

        with pytest.raises(ItemNotFound):
            await service.load_foo("bar")
