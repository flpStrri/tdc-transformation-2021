from uuid import uuid4

import bcrypt
from aiodynamo.client import Table
from fastapi.logger import logger

from domain.foo import Foo


class FooRepository:
    def __init__(self, dynamodb_table: Table):
        self.table = dynamodb_table

    @staticmethod
    def decode_foo(foo_table_item) -> Foo:
        if foo_table_item["type"] != "foo":
            raise ValueError("not a foo")

        foo_title: str = foo_table_item["title"]
        bcrypt.hashpw(foo_title.encode("utf-8"), bcrypt.gensalt(6))

        return Foo(
            identifier=foo_table_item["pk"],
            title=foo_title,
        )

    async def load_foo(self, identifier: str) -> Foo:
        request_id = uuid4().hex
        logger.info(f"{request_id} >> before loading foos/{identifier}")
        logger.info(f"{request_id}     >> I/O work on foos/{identifier}")
        foo_table_item = await self.table.get_item({"pk": identifier, "sk": "A"})
        logger.info(f"{request_id}     << I/O work on foos/{identifier}")
        logger.info(f"{request_id}     >> before CPU foos/{identifier}")
        decoded_foo = self.decode_foo(foo_table_item)
        logger.info(f"{request_id}     << after CPU foos/{identifier}")
        logger.info(f"{request_id} << after loading foos/{identifier}")
        return decoded_foo
