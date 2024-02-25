from typing import TYPE_CHECKING, List
import fastapi as _fastapi
import sqlalchemy.orm as _orm

import schemas as _schemas
import services as _services

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

app = _fastapi.FastAPI()

@app.post("/api/order_status",response_model=_schemas.Order_status)
async def create_order_status(
    order_status: _schemas.CreateOrder_status, 
    db: "Session" = _fastapi.Depends(_services.get_db)
):
    return await _services.create_order_status(order_status=order_status, db=db)

@app.get("/api/order_status",response_model=List[_schemas.Order_status])
async def get_order_status(db: "Session" = _fastapi.Depends(_services.get_db)):
    return await _services.get_order_status(db=db)

@app.get("/api/order_status/{order_status_id}",response_model=_schemas.Order_status)
async def get_order_statu(order_status_id: int, db: "Session" = _fastapi.Depends(_services.get_db)):
    order_status = await _services.get_order_statu(db=db, order_status_id=order_status_id)
    if order_status is None:
        raise _fastapi.HTTPException(status_code=404, detail="status doesnt exist")
    return await _services.get_order_statu(order_status_id=order_status_id, db=db)

@app.delete("/api/order_status/{order_status_id}")
async def delete_order_statu(order_status_id: int, db: "Session" = _fastapi.Depends(_services.get_db)):
    order_status = await _services.get_order_statu(db=db, order_status_id=order_status_id)
    if order_status is None:
        raise _fastapi.HTTPException(status_code=404, detail="status doesnt exist")
    await _services.delete_order_statu(order_status=order_status, db=db)

    return "Seccessfully deleted"

@app.put("/api/order_status/{order_status_id}",response_model=_schemas.Order_status)
async def update_order_status(order_status_id: int, 
                              order_status_data : _schemas.CreateOrder_status,
                              db: "Session" = _fastapi.Depends(_services.get_db)
                              ):
    order_status = await _services.get_order_statu(db=db, order_status_id=order_status_id)
    if order_status is None:
        raise _fastapi.HTTPException(status_code=404, detail="status doesnt exist")
    return await _services.update_order_statu(order_status=order_status,db=db,order_status_data=order_status_data)  