import random
from typing import TYPE_CHECKING, List
from faker import Faker

import database as _database
import model as _models
import sqlalchemy.orm as _orm

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



async def create_product(db: "Session"
) -> _schemas.Product:
    
    product_data = {"category_id": random.randint(1, 3), "name" : fake.word(), "description" : fake.text()}
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