from aiodynamo.client import Table

from domain.foo import Foo


class FooRepository:
    def __init__(self, dynamodb_table: Table):
        self.table = dynamodb_table

    @staticmethod
    def decode_foo(foo_table_item) -> Foo:
        if foo_table_item["type"] != "foo":
            raise ValueError("not a foo")

        return Foo(
            identifier=foo_table_item["pk"],
            title=foo_table_item["title"],
        )

    async def load_foo(self, identifier: str) -> Foo:
        foo_table_item = await self.table.get_item({"pk": identifier, "sk": "A"})
        decoded_foo = self.decode_foo(foo_table_item)
        return decoded_foo
