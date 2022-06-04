import json

from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models
from . import schemas


def get_shippers(db: Session):
    return db.query(models.Shipper).all()


def get_shipper(db: Session, shipper_id: int):
    return (
        db.query(models.Shipper).filter(models.Shipper.ShipperID == shipper_id).first()
    )


# 5.1
def get_suppliers(db: Session):
    return db.query(models.Supplier).all()


def get_supplier(db: Session, supplier_id: int):
    return db.query(models.Supplier).filter(models.Supplier.SupplierID == supplier_id).first()


# 5.2
def supplier_products(db: Session, supplier_id):
    return (
        db.query(
            models.Product.ProductID,
            models.Product.ProductName,
            models.Category.CategoryID,
            models.Category.CategoryName,
            models.Product.Discontinued,
        )
        .join(models.Category, models.Product.CategoryID == models.Category.CategoryID)
        .join(models.Supplier, models.Supplier.SupplierID == models.Product.SupplierID)
        .filter(models.Product.SupplierID == supplier_id)
        .order_by(models.Product.ProductID.desc())
        .all()
    )


# 5.3
def get_new_supplier_id(db: Session):
    row = db.query(func.max(models.Supplier.SupplierID)).first()
    new_id = row[0] + 1
    return new_id


def create_new_supplier(db: Session, supplier: schemas.SupplierPost):
    # **obj will unpack your dict object
    # User(**obj) will do like User(id=1, name='Awesome')
    dict_obj_supplier = dict(supplier)
    new_supplier = models.Supplier(**dict_obj_supplier)
    db.add(new_supplier)
    db.commit()


# 5.4
def change_existing_supplier(db: Session, supplier_id: int, customer: schemas.SupplierChanges):
    # remove given None values from json object
    values_to_change = {key: value for key, value in dict(customer).items() if value is not None}

    if values_to_change:
        db.query(models.Supplier).filter(
            models.Supplier.SupplierID == supplier_id
        ).update(values=values_to_change)
        db.commit()


# 5.5
def delete_existing_supplier(db: Session, supplier_id: int):
    db.query(models.Supplier).filter(
        models.Supplier.SupplierID == supplier_id
    ).delete()
    db.commit()
