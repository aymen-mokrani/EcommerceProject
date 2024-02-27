from main import app
from database import con
import schemas

@app.post("/api/product")
async def create_product():

    return 


@app.get("/api/product")
async def get_products():
    with con.cursor() as conn :
        
        products = conn.execute("SELECT * FROM gender;")
        
    print( products)
    
            

# @app.get("/api/product/{product_id}")
# async def get_product(product_id: int):
#     product = await _services.get_product(db=db, product_id=product_id)
#     if product is None:
#         raise _fastapi.HTTPException(status_code=404, detail="product doesnt exist")
#     return await _services.get_product(product_id=product_id, db=db)

# @app.delete("/api/product/{product_id}")
# async def delete_product(product_id: int, db: "Session" = _fastapi.Depends(_services.get_db)):
#     product = await _services.get_product(db=db, product_id=product_id)
#     if product is None:
#         raise _fastapi.HTTPException(status_code=404, detail="status doesnt exist")
#     await _services.delete_product(product=product, db=db)

#     return "Seccessfully deleted"

# @app.put("/api/product/{product_id}",response_model=_schemas.Product)
# async def update_product(product_id: int, 
#                               product_data : _schemas.CreateProduct,
#                               db: "Session" = _fastapi.Depends(_services.get_db)
#                               ):
#     product = await _services.get_product(db=db, product_id=product_id)
#     if product is None:
#         raise _fastapi.HTTPException(status_code=404, detail="status doesnt exist")
#     return await _services.update_product(product=product,db=db,product_data=product_data)  