import os
from typing import List
import sqlite3
from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from db import crud, schemas, models
from db.database import get_db
from pydantic import BaseModel

router = APIRouter()


class Customer(BaseModel):
    company_name: str


@router.on_event("startup")
async def startup():
    path = os.path.abspath(os.getcwd())
    router.db_connection = sqlite3.connect(os.path.join(path, "db_northwind/northwind.db"))
    router.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific


@router.on_event("shutdown")
async def shutdown():
    router.db_connection.close()


@router.get("/data")
async def root():
    cursor = await router.db_connection.execute("....")
    data = await cursor.fetchall()
    return {"data": data}


@router.get("/shippers/{shipper_id}", response_model=schemas.Shipper)
async def get_shipper(shipper_id: PositiveInt, db: Session = Depends(get_db)):
    db_shipper = crud.get_shipper(db, shipper_id)
    if db_shipper is None:
        raise HTTPException(status_code=404, detail="Shipper not found")
    return db_shipper


@router.get("/shippers", response_model=List[schemas.Shipper])
async def get_shippers(db: Session = Depends(get_db)):
    return crud.get_shippers(db)
