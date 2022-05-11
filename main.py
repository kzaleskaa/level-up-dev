from fastapi import FastAPI
from routers import task_1

app = FastAPI()

app.include_router(task_1.router)


#
# @app.post("/method", status_code=201)
# def method():
#     return {"method": "POST"}
#
# #
# # @app.get("/day/{name}/{number}")
# # async def day():
#     days = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}
