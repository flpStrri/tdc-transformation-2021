from application.foo_repository import FooRepository
from domain.foo import Foo


class FooService:
    def __init__(self, foo_repository: FooRepository):
        self.__foo_repository = foo_repository

    async def load_foo(self, identifier: str) -> Foo:
        return await self.__foo_repository.load_foo(identifier)
