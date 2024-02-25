from typing import TYPE_CHECKING, List

import database as _database
import model as _models
import sqlalchemy.orm as _orm

import schemas as _schemas
import services as _services

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

async def create_order_status(order_status: _schemas.CreateOrder_status, db: "Session"
) -> _schemas.Order_status:
    order_status = _models.order_status(**order_status.dict())
    db.add(order_status)
    db.commit()
    db.refresh(order_status)
    return _schemas.Order_status.from_orm(order_status)

async def get_order_status(db: "Session") -> List[_schemas.Order_status]:
    order_status = db.query(_models.order_status).all()
    return list(map(_schemas.Order_status.from_orm, order_status))

async def get_order_statu(order_status_id: int, db: "Session"):
    order_status = db.query(_models.order_status).filter(_models.order_status.id == order_status_id).first()
    return order_status

async def delete_order_statu(order_status: _models.order_status, db: "Session"):
    db.delete(order_status)
    db.commit()

async def update_order_statu(order_status: _models.order_status, 
                             db: "Session", 
                             order_status_data = _schemas.CreateOrder_status)-> _schemas.Order_status:
    
    order_status.status = order_status_data.status
    db.commit()
    db.refresh(order_status)
    return _schemas.Order_status.from_orm(order_status)