from pydantic import BaseModel


class Foo(BaseModel):
    identifier: str
    title: str
