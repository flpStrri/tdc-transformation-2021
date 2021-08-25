import pytest
from httpx import AsyncClient

from presentation.rest_api.main import app
from tests.infrastructure.database.dynamo_db_test_wrapper import DynamoDBWrapper

pytestmark = pytest.mark.asyncio


class TestGetProduct(DynamoDBWrapper):
    async def test_should_return_bar_response_given_row_present_in_database(self, data_table):
        await data_table.put_item(
            {"pk": "bar", "sk": "A", "name": "Bar"},
        )
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/products/bar")

        assert {"identifier": "bar", "name": "Bar"} == response.json()

    async def test_should_return_404_response_given_row_not_present_in_database(self, data_table):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/products/bar")

        assert 404 == response.status_code
