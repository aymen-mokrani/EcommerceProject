from datetime import datetime
from uuid import uuid4 as uuid
from fastapi import APIRouter,HTTPException
from database import init_connection
import schemas

con=init_connection()
router = APIRouter()

def insert_gender(gender_type : str,):
    sql_gender = "INSERT INTO gender(gender_type) VALUES(%s) RETURNING id;"
    with  con.cursor() as conn :
        conn.execute("SELECT * FROM gender WHERE gender_type = (%s)", (gender_type,))
        exist_gender = conn.fetchone()
        if exist_gender:
            return exist_gender[0]
            
        conn.execute(sql_gender, (gender_type,))
        
        gender_id = conn.fetchone()[0]
        
    return gender_id

def insert_style(style_name : str,):
    sql_style = "INSERT INTO style(style_name) VALUES(%s) RETURNING id;"
    with  con.cursor() as conn :
        conn.execute("SELECT * FROM style WHERE style_name = (%s)", (style_name,))
        exist_style = conn.fetchone()
        if exist_style:
            return exist_style[0]
            
        conn.execute(sql_style, (style_name,))
        style_id = conn.fetchone()[0]
        
    return style_id

def insert_category(category_name : str, gender_id : int,style_id : int,):
    sql_category = "INSERT INTO category(category_name,gender_id,style_id) VALUES(%s,%s,%s) RETURNING id;"
    with  con.cursor() as conn :
        conn.execute("SELECT * FROM category WHERE category_name = (%s)", (category_name,))
        exist_category = conn.fetchone()
        if exist_category:
            return exist_category[0]
            
        conn.execute(sql_category, (category_name, gender_id,style_id,))
        category_id = conn.fetchone()[0]

    return category_id

def insert_color(color_name : str,):
    sql_color = "INSERT INTO color(color_name) VALUES(%s) RETURNING id;"
    with  con.cursor() as conn :
        conn.execute("SELECT * FROM color WHERE color_name = (%s)", (color_name,))
        exist_color = conn.fetchone()
        if exist_color:
            return exist_color[0]
            
        conn.execute(sql_color, (color_name,))
        color_id = conn.fetchone()[0]
        
    return color_id

def insert_size(size : str,):
    sql_size = "INSERT INTO size(size) VALUES(%s) RETURNING id;"
    with  con.cursor() as conn :
        conn.execute("SELECT * FROM size WHERE size = (%s)", (size,))
        exist_size = conn.fetchone()
        if exist_size:
            return exist_size[0]
            
        conn.execute(sql_size, (size,))
        size_id = conn.fetchone()[0]
        
    return size_id

def insert_stock_quantity(quantity : int,):
    sql_stock_quantity = "INSERT INTO stock_quantity(quantity,created_at) VALUES(%s,%s) RETURNING id;"
    with  con.cursor() as conn :
        conn.execute(sql_stock_quantity, (quantity, datetime.now(),))
        stock_quantity_id = conn.fetchone()[0]
        
    return stock_quantity_id


def insert_product(name : str, description : str, gender_type : str , style_name : str, category_name : str,):

    sql_product = "INSERT INTO product(category_id,name,description) VALUES(%s,%s,%s) RETURNING id;"

    with  con.cursor() as conn :
        
        conn.execute("SELECT * FROM product WHERE name = (%s)", (name,))
        exist_product = conn.fetchone()
        if exist_product:
            return exist_product[0]
            
        gender_id = insert_gender(gender_type)
            
        style_id = insert_style(style_name)

        category_id = insert_category(category_name,gender_id,style_id)
           
        conn.execute(sql_product, (category_id, name, description,))   
        product_id = conn.fetchone()[0]

    return product_id

@router.post("/product/add", response_model=str)
async def create_product_item(Product_item : schemas._Product_item, 
                              Product : schemas._Product,
                              Stock_quantity : schemas._Stock_quantity, 
                              Category : schemas._Category, 
                              Size : schemas._size, 
                              Color : schemas._Color , 
                              Style : schemas._Style, 
                              Gender : schemas._Gender):
    
    sql_product_item = """INSERT INTO product_item(product_id,color_id,size_id,sku,price,stock_quantity_id) 
                        VALUES(%s,%s,%s,%s,%s,%s) 
                        RETURNING id;"""
    with  con.cursor() as conn :
        try:
            color_id = insert_color(Color.color_name)
            size_id = insert_size(Size.size)
            stock_quantity_id = insert_stock_quantity(Stock_quantity.quantity)
            Product_id = insert_product(Product.name, 
                                        Product.description, 
                                        Gender.gender_type, 
                                        Style.style_name, 
                                        Category.category_name,)
            

            conn.execute(sql_product_item, 
                         (Product_id, 
                          color_id, 
                          size_id, 
                          str(uuid()), 
                          Product_item.price, 
                          stock_quantity_id,))
               
            product_item_id = conn.fetchone()[0]
            
        except Exception as e:
            con.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred while processing your request {e}",
            )

        con.commit()
        return "product item added successefully"