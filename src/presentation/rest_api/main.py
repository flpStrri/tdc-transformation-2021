import logging
from uuid import uuid4

import bcrypt
from aiodynamo.errors import ItemNotFound
from fastapi import FastAPI, HTTPException
from fastapi.logger import logger
from fastapi.responses import JSONResponse

from domain.product import Product
from infrastructure.aiohttp import get_aiohttp_client
from infrastructure.database import data_table

app = FastAPI()
fast_api_logger = logger


@app.get("/products/{product_id}")
async def get_product(product_id: str):
    async with get_aiohttp_client() as client:
        dynamodb_table = data_table(client)
        request_id = uuid4().hex
        logger.info(f"{request_id} >> before loading products/{product_id}")
        try:
            logger.info(f"{request_id}     >> I/O work on products/{product_id}")
            table_item = await dynamodb_table.get_item({"pk": product_id, "sk": "A"})
            logger.info(f"{request_id}     << I/O work on products/{product_id}")

            logger.info(f"{request_id}     >> before CPU products/{product_id}")
            bcrypt.hashpw(table_item["name"].encode("utf-8"), bcrypt.gensalt(6))
            product = Product(
                identifier=table_item["pk"],
                name=table_item["name"],
            )
            logger.info(f"{request_id}     << after CPU products/{product_id}")

            logger.info(f"{request_id} << after loading products/{product_id}")
            return JSONResponse(product.dict())
        except ItemNotFound:
            raise HTTPException(status_code=404, detail="product not found")


if __name__ != "main":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    logger.handlers = gunicorn_logger.handlers
    logger.setLevel(gunicorn_logger.level)
