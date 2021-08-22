from aiodynamo.client import Client, Table
from aiodynamo.credentials import Credentials
from aiodynamo.http.aiohttp import AIOHTTP

from infrastructure.service_parameters import parameters


def data_table(aioclient) -> Table:
    dynamodb = Client(
        AIOHTTP(aioclient),
        Credentials.auto(),
        region=parameters.region,
        endpoint=parameters.dynamodb_url,
    )
    return dynamodb.table(parameters.service_data_table_name)
