import os
from typing import List
import sqlite3
from sqlalchemy.sql.expression import func
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


# 5.1
@router.get("/suppliers/{supplier_id}", response_model=schemas.Supplier, status_code=200)
async def get_supplier(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier


@router.get("/suppliers", response_model=List[schemas.SupplierBasic])
async def get_suppliers(db: Session = Depends(get_db)):
    return crud.get_suppliers(db)


# 5.2
@router.get("/suppliers/{supplier_id}/products", status_code=200)
async def get_supplier_products(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    router.db_connection.row_factory = sqlite3.Row
    db_supplier = crud.get_supplier(db, supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")

    data = crud.supplier_products(db, supplier_id)
    return [
            {
                "ProductID": x["ProductID"],
                "ProductName": x["ProductName"],
                "Category": {"CategoryID": x["CategoryID"], "CategoryName": x["CategoryName"]},
                "Discontinued": x["Discontinued"]
            } for x in data
    ]


# 5.3
@router.post("/suppliers", response_model=schemas.Supplier, status_code=200)
async def customer_add(supplier: schemas.SupplierPost, db: Session = Depends(get_db)):
    router.db_connection.row_factory = sqlite3.Row
    if supplier.SupplierID is None:
        new_supplier_id = db.query(func.max(models.Supplier.SupplierID)).first()[0] + 1
        supplier.SupplierID = new_supplier_id

    crud.create_new_supplier(db, supplier)
    db_supplier = crud.get_supplier(db, new_supplier_id)
    return db_supplier


# 5.4
@router.put("/supplier/{supplier_id}", response_model=schemas.Supplier, status_code=200)
async def put_customer(response: Response, supplier_id: int, customer: schemas.SupplierChanges, db: Session = Depends(get_db)):
    router.db_connection.row_factory = sqlite3.Row
    db_supplier = crud.get_supplier(db, supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")

    crud.change_existing_supplier(db, supplier_id, customer)
    response.status_code = 200
    db_supplier = crud.get_supplier(db, supplier_id)

    return db_supplier


# 5.5
@router.delete("/supplier/{supplier_id}", status_code=204)
async def delete_customer(response: Response, supplier_id: int, db: Session = Depends(get_db)):
    router.db_connection.row_factory = sqlite3.Row
    db_supplier = crud.get_supplier(db, supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")

    crud.delete_existing_supplier(db, supplier_id)

    return Response(status_code=204)
