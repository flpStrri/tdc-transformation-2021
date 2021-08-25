import logging
from uuid import uuid4

import bcrypt
from aiodynamo.errors import ItemNotFound
from fastapi import FastAPI, HTTPException
from fastapi.logger import logger
from fastapi.responses import JSONResponse

from domain.foo import Foo
from infrastructure.aiohttp import get_aiohttp_client
from infrastructure.database import data_table

app = FastAPI()
fast_api_logger = logger


@app.get("/foos/{foo_id}")
async def get_foo(foo_id: str):
    async with get_aiohttp_client() as client:
        dynamodb_table = data_table(client)
        request_id = uuid4().hex
        logger.info(f"{request_id} >> before loading foos/{foo_id}")
        try:
            logger.info(f"{request_id}     >> I/O work on foos/{foo_id}")
            foo_table_item = await dynamodb_table.get_item({"pk": foo_id, "sk": "A"})
            logger.info(f"{request_id}     << I/O work on foos/{foo_id}")

            logger.info(f"{request_id}     >> before CPU foos/{foo_id}")
            bcrypt.hashpw(foo_table_item["title"].encode("utf-8"), bcrypt.gensalt(6))
            decoded_foo = Foo(
                identifier=foo_table_item["pk"],
                title=foo_table_item["title"],
            )
            logger.info(f"{request_id}     << after CPU foos/{foo_id}")

            logger.info(f"{request_id} << after loading foos/{foo_id}")
            return JSONResponse(decoded_foo.dict())
        except ItemNotFound:
            raise HTTPException(status_code=404, detail="foo not found")


if __name__ != "main":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    logger.handlers = gunicorn_logger.handlers
    logger.setLevel(gunicorn_logger.level)
