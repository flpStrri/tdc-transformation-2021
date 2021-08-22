from aiodynamo.errors import ItemNotFound
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from application.foo_service import FooService
from infrastructure.aiohttp import get_aiohttp_client
from infrastructure.database import data_table
from infrastructure.foo_repository import FooRepository

app = FastAPI()


@app.get("/foos/{foo_id}")
async def get_foo(foo_id: str):
    async with get_aiohttp_client() as client:
        foo_service = FooService(foo_repository=FooRepository(data_table(client)))
        try:
            loaded_foo = await foo_service.load_foo(identifier=foo_id)
            return JSONResponse(loaded_foo.dict())
        except ItemNotFound:
            raise HTTPException(status_code=404, detail="foo not found")
