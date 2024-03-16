from fastapi import APIRouter, HTTPException
from database import init_connection

con=init_connection()
router = APIRouter()

@router.get("/api/product")
async def get_products():
    
    with con.cursor() as conn :
        
        conn.execute("SELECT * FROM product;")
        products = conn.fetchall()
    
    return products

@router.get("/api/product/{product_id}")
async def get_product(product_id: int):
    
    with con.cursor() as conn :
        try:
            conn.execute("SELECT * FROM product WHERE id = (%s)", (product_id,))
            exist_product = conn.fetchone()
            if not exist_product:
                raise HTTPException(status_code=404, detail="product does not exist")
            return {"product": exist_product}

        except Exception as e:
            print(f"An error occurred while fetching product data: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        
@router.get("/api/product_item")
async def get_product_items():
    
    with con.cursor() as conn :
        conn.execute("SELECT * FROM product_item;")
        product_items = conn.fetchall()
    
    return product_items

@router.get("/api/product_item/{product_item_id}")
async def get_product_item(product_item_id: int):
    
    with con.cursor() as conn :
        try:
            conn.execute("SELECT * FROM product_item WHERE id = (%s)", (product_item_id,))
            exist_product_item = conn.fetchone()
            if not exist_product_item:
                raise HTTPException(status_code=404, detail="product_item does not exist")
            return {"product": exist_product_item}

        except Exception as e:
            print(f"An error occurred while fetching product data: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")