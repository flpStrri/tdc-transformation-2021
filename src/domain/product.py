from pydantic import BaseModel


class Product(BaseModel):
    identifier: str
    name: str
