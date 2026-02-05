from fastapi import FastAPI
from project.routes import router
from db import creat_table

app = FastAPI()

app.include_router(
    router,
    
)