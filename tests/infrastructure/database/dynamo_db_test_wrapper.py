from unittest.mock import patch

from aiodynamo.client import Client
from aiodynamo.credentials import Credentials
from aiodynamo.http.aiohttp import AIOHTTP
from aiodynamo.models import KeySchema, KeySpec, KeyType, Throughput
from pytest import fixture

from infrastructure.aiohttp import get_aiohttp_client
from infrastructure.service_parameters import parameters


class DynamoDBWrapper:
    @fixture
    async def data_table(self):
        with patch.dict(
            "os.environ",
            {
                "DATA_TABLE": "tdc-dev-data",
                "AWS_ACCESS_KEY_ID": "local-key",
                "AWS_SECRET_ACCESS_KEY": "local-secret",
            },
        ):
            async with get_aiohttp_client() as client:
                dynamodb = Client(
                    AIOHTTP(client),
                    Credentials.auto(),
                    parameters.region,
                    parameters.dynamodb_url,
                )
                table = dynamodb.table(parameters.service_data_table_name)
                if await table.exists():
                    await table.delete(wait_for_disabled=True)
                await table.create(
                    Throughput(read=10, write=10),
                    KeySchema(
                        hash_key=KeySpec("pk", KeyType.string),
                        range_key=KeySpec("sk", KeyType.string),
                    ),
                    wait_for_active=True,
                )
                yield table

                await table.delete(wait_for_disabled=True)
