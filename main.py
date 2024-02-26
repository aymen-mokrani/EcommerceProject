from typing import TYPE_CHECKING, List
import fastapi as _fastapi
import sqlalchemy.orm as _orm


import schemas as _schemas
import services as _services

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

app = _fastapi.FastAPI()


@app.post("/api/product",response_model=_schemas.Product)
async def create_product( 
    db: "Session" = _fastapi.Depends(_services.get_db)
):
    return await _services.create_product(db=db)


@app.get("/api/product",response_model=List[_schemas.Product])
async def get_products(db: "Session" = _fastapi.Depends(_services.get_db)):
    return await _services.get_products(db=db)

@app.get("/api/product/{product_id}",response_model=_schemas.Product)
async def get_product(product_id: int, db: "Session" = _fastapi.Depends(_services.get_db)):
    product = await _services.get_product(db=db, product_id=product_id)
    if product is None:
        raise _fastapi.HTTPException(status_code=404, detail="product doesnt exist")
    return await _services.get_product(product_id=product_id, db=db)

@app.delete("/api/product/{product_id}")
async def delete_product(product_id: int, db: "Session" = _fastapi.Depends(_services.get_db)):
    product = await _services.get_product(db=db, product_id=product_id)
    if product is None:
        raise _fastapi.HTTPException(status_code=404, detail="status doesnt exist")
    await _services.delete_product(product=product, db=db)

    return "Seccessfully deleted"

@app.put("/api/product/{product_id}",response_model=_schemas.Product)
async def update_product(product_id: int, 
                              product_data : _schemas.CreateProduct,
                              db: "Session" = _fastapi.Depends(_services.get_db)
                              ):
    product = await _services.get_product(db=db, product_id=product_id)
    if product is None:
        raise _fastapi.HTTPException(status_code=404, detail="status doesnt exist")
    return await _services.update_product(product=product,db=db,product_data=product_data)  