from pydantic import BaseModel, PositiveInt, constr
from typing import Optional


class Shipper(BaseModel):
    ShipperID: PositiveInt
    CompanyName: constr(max_length=40)
    Phone: constr(max_length=24)

    class Config:
        orm_mode = True


class SupplierBasic(BaseModel):
    SupplierID: PositiveInt
    CompanyName: constr(max_length=40)

    class Config:
        orm_mode = True


class Supplier(BaseModel):
    SupplierID: PositiveInt
    CompanyName: constr(max_length=40)
    ContactName: Optional[constr(max_length=30)]
    ContactTitle: Optional[constr(max_length=30)]
    Address: Optional[constr(max_length=60)]
    City: Optional[constr(max_length=15)]
    Region: Optional[constr(max_length=15)]
    PostalCode: Optional[constr(max_length=10)]
    Country: Optional[constr(max_length=15)]
    Phone: Optional[constr(max_length=24)]
    Fax: Optional[constr(max_length=24)]
    HomePage: Optional[str]

    class Config:
        orm_mode = True


class Product(BaseModel):
    ProductId: PositiveInt
    SupplierId: PositiveInt

    class Config:
        orm_mode = True


class SupplierPost(BaseModel):
    SupplierID: Optional[PositiveInt]
    CompanyName: constr(max_length=40)
    ContactName: Optional[constr(max_length=30)]
    ContactTitle: Optional[constr(max_length=30)]
    Address: Optional[constr(max_length=60)]
    City: Optional[constr(max_length=15)]
    Region: Optional[constr(max_length=15)]
    PostalCode: Optional[constr(max_length=10)]
    Country: Optional[constr(max_length=15)]
    Phone: Optional[constr(max_length=24)]
    Fax: Optional[constr(max_length=24)]
    HomePage: Optional[str]

    class Config:
        orm_mode = True


class SupplierChanges(BaseModel):
    CompanyName: Optional[constr(max_length=40)]
    ContactName: Optional[constr(max_length=30)]
    ContactTitle: Optional[constr(max_length=30)]
    Address: Optional[constr(max_length=60)]
    City: Optional[constr(max_length=15)]
    Region: Optional[constr(max_length=15)]
    PostalCode: Optional[constr(max_length=10)]
    Country: Optional[constr(max_length=15)]
    Phone: Optional[constr(max_length=24)]
    Fax: Optional[constr(max_length=24)]
    HomePage: Optional[str]

    class Config:
        orm_mode = True
