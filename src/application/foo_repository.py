from typing import Protocol

from domain.foo import Foo


class FooRepository(Protocol):  # pragma: no cover
    async def load_foo(self, identifier: str) -> Foo:
        pass
