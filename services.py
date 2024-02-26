import random
from typing import TYPE_CHECKING, List
from faker import Faker

import database as _database
import model as _models

import schemas as _schemas

fake = Faker()


if TYPE_CHECKING:
    from sqlalchemy.orm import Session

def _add_tables():
    return _database.base.metadata.create_all(bind =_database.engine)

def get_db():
    db = _database.sessionLocal()
    try :
        yield db
    finally:
        db.close()


#PRODUCT
        
async def create_product(db: "Session"
) -> _schemas.Product:
    
    product_data = { "category_id": random.randint(1, 3)
                    ,"name" : fake.word()
                    ,"description" : fake.text()}
    product = _schemas.CreateProduct(**product_data)
    product = _models.product(**product.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return _schemas.Product.from_orm(product)

async def get_products(db: "Session") -> List[_schemas.Product]:
    product = db.query(_models.product).all()
    return list(map(_schemas.Product.from_orm, product))

async def get_product(product_id: int, db: "Session"):
    product = db.query(_models.product).filter(_models.product.id == product_id).first()
    return product

async def delete_product(product: _models.product, db: "Session"):
    db.delete(product)
    db.commit()

async def update_product(product: _models.product, 
                             db: "Session", 
                             product_data = _schemas.CreateProduct)-> _schemas.Product:
    
    product.category_id = product_data.category_id
    product.description = product_data.description
    product.name = product_data.name
    db.commit()
    db.refresh(product)
    return _schemas.Product.from_orm(product)

#ADDRESS

async def create_address(db: "Session"
) -> _schemas.Address:
    
    address_data = { "unit_number":  fake.building_number() 
                    ,"street_number": fake.building_number()
                    ,"address_line": fake.street_address()
                    ,"city" : fake.city()
                    ,"region" : fake.state()
                    ,"postal_code" : fake.postcode()
                    ,"country_id" : random.randint(1, 192)}
    address = _schemas.CreateAddress(**address_data)
    address = _models.address(**address.dict())
    db.add(address)
    db.commit()
    db.refresh(address)
    return _schemas.Address.from_orm(address)

async def get_addresses(db: "Session") -> List[_schemas.Address]:
    address = db.query(_models.address).all()
    return list(map(_schemas.Address.from_orm, address))

async def get_address(address_id: int, db: "Session"):
    address = db.query(_models.address).filter(_models.address.id == address_id).first()
    return address

async def delete_address(address: _models.address, db: "Session"):
    db.delete(address)
    db.commit()

async def update_address(address: _models.address, 
                             db: "Session", 
                             address_data = _schemas.CreateAddress)-> _schemas.Address:
    
    address.unit_number = address_data.unit_number
    address.street_number = address_data.street_number
    address.address_line = address_data.address_line
    address.city = address_data.city
    address.region = address_data.region
    address.postal_code = address_data.postal_code
    address.country_id  = address_data.country_id

    db.commit()
    db.refresh(address)
    return _schemas.Address.from_orm(address)