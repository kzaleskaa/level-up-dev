from fastapi import FastAPI
from routers import task_1

app = FastAPI()

app.include_router(task_1.router)


