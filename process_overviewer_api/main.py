import uvicorn
import logging
from fastapi import FastAPI

po_app = FastAPI()


@po_app.get("/ping/")
async def ping():
    return {"data": "Ping successful :-)"}


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("process_overviewer_api.main:po_app",
                host="127.0.0.1",
                port=8700,
                reload=True)


if __name__ == "__name__":
    start()