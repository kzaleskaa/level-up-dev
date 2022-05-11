from fastapi import APIRouter, Request, Response
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from datetime import date


router = APIRouter()

router.counter = 0


class Event(BaseModel):
    id: int = router.counter
    date: date
    name: str
    date_added: date = date.today()


@router.get("/", status_code=200)
def root():
    return {"start": "1970-01-0"}

@router.api_route("/method", methods=["GET", "PUT", "OPTIONS", "DELETE", "POST"])
async def method(response: Response, request: Request):
    if request.method == "POST":
        response.status_code = 201
    else:
        response.status_code = 200
    return {"method": request.method}

@router.get("/day")
def day(response: Response, name: str, number: int):
    days = {1: "monday", 2: "tuesday", 3: "wednesday", 4: "thursday", 5: "friday", 6: "saturday", 7: "sunday"}

    if days[number] == name.lower():
        response.status_code = 200
    else:
        response.status_code = 400

@router.put("/events", status_code=201)
async def events(event: Event):
    update_event = jsonable_encoder(event)
    update_event["id"] = router.counter
    router.counter += 1
    return update_event

# @router.get("/event/{date}")
# async def events_by_date(date: date):
#     events = Event(date=date)
#     # update_event = jsonable_encoder(events)
#     return {"events": events}
