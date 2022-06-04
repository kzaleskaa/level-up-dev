from sqlalchemy.orm import Session

from . import models
from . import schemas


def get_shippers(db: Session):
    return db.query(models.Shipper).all()


def get_shipper(db: Session, shipper_id: int):
    return (
        db.query(models.Shipper).filter(models.Shipper.ShipperID == shipper_id).first()
    )


def get_suppliers(db: Session):
    return db.query(models.Supplier).all()


def get_supplier(db: Session, supplier_id: int):
    return (
        db.query(models.Supplier).filter(models.Supplier.SupplierID == supplier_id).first()
    )


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


def create_new_supplier(db: Session, supplier: schemas.SupplierPost):
    new_supplier = models.Supplier(**dict(supplier))
    db.add(new_supplier)
    db.commit()


def change_existing_supplier(db: Session, supplier_id: int, changes: schemas.SupplierChanges):
    db.query(models.Supplier).filter(
        models.Supplier.SupplierID == supplier_id
    ).update(values={"CompanyName": changes.CompanyName, "ContactName": changes.ContactName})
    db.commit()


def delete_existing_supplier(db: Session, supplier_id: int):
    db.query(models.Supplier).filter(
        models.Supplier.SupplierID == supplier_id
    ).delete()
    db.commit()
