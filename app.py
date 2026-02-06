from fastapi import FastAPI
from project.routes import router
from db import creat_table

app = FastAPI()

@app.on_event("startup")
async def on_startup() -> None:
    await creat_table()

app.include_router(
    router
)
