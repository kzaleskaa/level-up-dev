from fastapi import APIRouter, Request, Response
from pydantic import BaseModel
from datetime import date
from typing import List
import datetime
from datetime import datetime

router = APIRouter()
router.counter = 0
router.data = []


class Event(BaseModel):
    date: str
    event: str


class NewEvent(BaseModel):
    id: int
    name: str
    date: str
    date_added: str


# 1.1
@router.get("/", status_code=200)
def root():
    return {"start": "1970-01-01"}


# 1.2
@router.api_route("/method", methods=["GET", "PUT", "OPTIONS", "DELETE", "POST"])
def method(response: Response, request: Request):
    if request.method == "POST":
        response.status_code = 201
    else:
        response.status_code = 200
    return {"method": request.method}


# 1.3
@router.get("/day", status_code=200)
def day(response: Response, name: str, number: int):
    days = {1: "monday", 2: "tuesday", 3: "wednesday", 4: "thursday", 5: "friday", 6: "saturday", 7: "sunday"}

    if number in days:
        if days[number] == name.lower():
            response.status_code = 200
        else:
            response.status_code = 400
    else:
        response.status_code = 400


# 1.4
@router.put("/events", status_code=200, response_model=NewEvent)
def events(response: Response, event_item: Event):
    if bool(datetime.strptime(str(event_item.date), "%Y-%m-%d")):
        router.counter += 1

        new_event = NewEvent(id=router.counter, name=event_item.event, date=str(event_item.date), date_added=str(date.today()))
        router.data.append(new_event)

        return new_event
    else:
        response.status_code = 400


# 1.5
@router.get("/events/{event_date}", status_code=200, response_model=List[NewEvent])
def get_event_by_date(event_date: str, response: Response):
    events_list = []

    try:
        res = bool(datetime.strptime(event_date, "%Y-%m-%d"))
        events_list = [event for event in router.data if event.date == str(event_date)]

        if len(events_list) == 0:
            response.status_code = 404

    except ValueError:
        response.status_code = 400

    return events_list
