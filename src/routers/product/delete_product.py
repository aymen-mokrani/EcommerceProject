from datetime import datetime
from fastapi import APIRouter,HTTPException
from database import init_connection
import schemas

con=init_connection()
router = APIRouter()

def delete_stock_quantity(stock_quantity_id : int,):
    sql_stock_quantity = "UPDATE stock_quantity SET deleted_at = %s WHERE id =% s;"
    with  con.cursor() as conn :
        conn.execute(sql_stock_quantity, ( datetime.now(), stock_quantity_id,))
        stock_quantity_id = conn.fetchone()[0]
        
    return stock_quantity_id

def delete_Product(product_id : int,):

    sql_product = "DELETE FROM product WHERE product_id = (%s);"

    with  con.cursor() as conn :
        
        exist_product = conn.fetchone()
        if not exist_product:
            raise HTTPException(status_code=404, detail="product does not exist")
            
           
        conn.execute(sql_product, (product_id,))   
        product_id = conn.fetchone()[0]
        con.commit()

    return product_id


@router.delete("/product/delete_product/{product_id}")
async def delete_product(product_id:int,):

    with  con.cursor() as conn :
        try:
            delete_product(product_id)
            con.commit()
            print("product deleted successefully")

        except Exception as e:
            con.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred while processing your request {e}",
            )
 

@router.delete("/product/delete_product_item/{Product_item_id}")
async def delete_product_item(Product_item_id : int,):
    
    sql_product_item = """DELETE FROM product_item WHERE id = (%s)"""

    with  con.cursor() as conn :
        try:
            
            conn.execute("SELECT product_id FROM product_item WHERE id = (%s)", (Product_item_id,))
            Product_id = conn.fetchone()[0]

            conn.execute(sql_product_item, 
                         (Product_item_id,))
               
            delete_Product(Product_id)
            con.commit()

        except Exception as e:
            con.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred while processing your request {e}",
            )

        con.commit()
        return "product item deleted successefully"