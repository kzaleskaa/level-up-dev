from fastapi import APIRouter, Request, Response
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date
from fastapi.encoders import jsonable_encoder
from typing import List

app = FastAPI()
app.counter = -1
app.data = []

class Event(BaseModel):
    date: date
    name: str

@app.get("/", status_code=200)
def root():
    return {"start": "1970-01-0"}

@app.api_route("/method", methods=["GET", "PUT", "OPTIONS", "DELETE", "POST"])
def method(response: Response, request: Request):
    if request.method == "POST":
        response.status_code = 201
    else:
        response.status_code = 200
    return {"method": request.method}

@app.get("/day")
def day(response: Response, name: str, number: int):
    days = {1: "monday", 2: "tuesday", 3: "wednesday", 4: "thursday", 5: "friday", 6: "saturday", 7: "sunday"}

    if days[number] == name.lower():
        response.status_code = 200
    else:
        response.status_code = 400

@app.put("/events", status_code=200)
def events(event: Event):
    update_event = jsonable_encoder(event)
    app.counter += 1
    app.data.append({"id": app.counter, "event": update_event["name"], "date": str(update_event["date"]), "date_added":str(date.today())})
    return {"id": app.counter, "event": update_event["name"], "date": update_event["date"], "date_added":date.today()}

@app.get("/event/{event_date}")
def get_event_by_date(event_date: date):
    events = [event for event in app.data if event["date"]==str(event_date)]
    return events

