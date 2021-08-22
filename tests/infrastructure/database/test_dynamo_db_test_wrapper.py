import pytest
from aiodynamo.client import Table

from tests.infrastructure.database.dynamo_db_test_wrapper import DynamoDBWrapper

pytestmark = pytest.mark.asyncio


class TestDynamoDBWrapper(DynamoDBWrapper):
    async def test_should_have_no_values(self, data_table: Table):
        assert len((await data_table.scan_single_page()).items) == 0

    async def test_should_have_really_no_values(self, data_table: Table):
        async for page in data_table.scan():
            assert page.items() == []

    async def test_should_add_table_item(self, data_table):
        assert len((await data_table.scan_single_page()).items) == 0
        await data_table.put_item(
            {"pk": "a_good_hash_key", "sk": "any_other_value"},
        )
        assert len((await data_table.scan_single_page()).items) == 1

    async def test_should_still_have_no_values(self, data_table):
        assert len((await data_table.scan_single_page()).items) == 0
