import pytest
from aiodynamo.client import Table
from aiodynamo.errors import ItemNotFound

from domain.foo import Foo
from infrastructure.foo_repository import FooRepository
from tests.infrastructure.foo_repository.foo_repository_fixtures import FooRepositoryFixtures

pytestmark = pytest.mark.asyncio


class TestLoadFoo(FooRepositoryFixtures):
    async def test_should_raise_if_not_found(
        self, repository: FooRepository, data_table: Table, fake
    ):
        assert len((await data_table.scan_single_page()).items) == 0
        with pytest.raises(ItemNotFound):
            await repository.load_foo(fake.uuid4())

    async def test_should_raise_if_unexpected_type_found(
        self, repository: FooRepository, data_table: Table, fake
    ):
        foo_identifier = fake.uuid4()
        foo_item = {
            "pk": foo_identifier,
            "sk": "A",
            "type": "bar",
            "title": fake.catch_phrase(),
        }
        await data_table.put_item(foo_item)
        with pytest.raises(ValueError, match="not a foo"):
            await repository.load_foo(foo_identifier)

    async def test_should_return_foo_if_found(
        self, repository: FooRepository, data_table: Table, fake
    ):
        foo_identifier = fake.uuid4()
        foo_item = {
            "pk": foo_identifier,
            "sk": "A",
            "type": "foo",
            "title": fake.catch_phrase(),
        }
        await data_table.put_item(foo_item)
        loaded_foo = await repository.load_foo(foo_identifier)
        assert loaded_foo == Foo(
            identifier=foo_item["pk"],
            title=foo_item["title"],
        )
