from fastapi import FastAPI
from routers import router, fast

app = FastAPI()

app.include_router(router.router, tags=["task-1"])
app.include_router(fast.router, tags=["task-3"])