from contextlib import asynccontextmanager
from socket import AF_INET

import aiohttp

SIZE_POOL_AIOHTTP = 100


@asynccontextmanager
async def get_aiohttp_client():
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=2),
        connector=aiohttp.TCPConnector(family=AF_INET, limit_per_host=SIZE_POOL_AIOHTTP),
    ) as client:
        yield client
