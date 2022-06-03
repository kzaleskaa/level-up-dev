from fastapi import FastAPI
from routers import router, fast, northwind

app = FastAPI()

app.include_router(router.router, tags=["task-1"])
app.include_router(fast.router, tags=["task-3"])
app.include_router(northwind.router, tags=["northwind"])
