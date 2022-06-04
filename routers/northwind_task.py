import sqlite3
from typing import List
from sqlalchemy.sql.expression import func
from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import PositiveInt
from sqlalchemy.orm import Session
from db import crud, schemas, models
from db.database import get_db

router = APIRouter()


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
    # check supplier's id
    db_supplier = crud.get_supplier(db, supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")

    # create list of products
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
@router.post("/suppliers", response_model=schemas.Supplier, status_code=201)
async def customer_add(supplier: schemas.SupplierPost, db: Session = Depends(get_db)):
    if supplier.SupplierID is None:
        new_supplier_id = crud.get_new_supplier_id(db)
        supplier.SupplierID = new_supplier_id

    crud.create_new_supplier(db, supplier)
    db_supplier = crud.get_supplier(db, new_supplier_id)
    return db_supplier


# 5.4
@router.put("/suppliers/{supplier_id}", response_model=schemas.Supplier, status_code=200)
async def put_customer(response: Response, supplier_id: int, customer: schemas.SupplierChanges, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")

    crud.change_existing_supplier(db, supplier_id, customer)
    db_supplier = crud.get_supplier(db, supplier_id)
    return db_supplier


# 5.5
@router.delete("/suppliers/{supplier_id}", status_code=204)
async def delete_customer(supplier_id: int, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")

    crud.delete_existing_supplier(db, supplier_id)
