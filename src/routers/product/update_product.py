from datetime import datetime
from fastapi import APIRouter,HTTPException
from database import init_connection
import schemas

con=init_connection()
router = APIRouter()

def update_gender(updated_gender_type):
    sql_gender = "INSERT INTO gender(gender_type) VALUES(%s)RETURNING id;"
    with  con.cursor() as conn :
        conn.execute("SELECT * FROM gender WHERE gender_type = (%s)", (updated_gender_type,))
        exist_gender = conn.fetchone()
        if exist_gender:
            return exist_gender[0]
            
        conn.execute(sql_gender, (updated_gender_type,))
        gender_id = conn.fetchone()[0]

    return gender_id

def update_style(updated_style_name):
    sql_style = "INSERT INTO style(style_name) VALUES(%s) RETURNING id;"
    with  con.cursor() as conn :
        conn.execute("SELECT * FROM style WHERE style_name = (%s)", (updated_style_name,))
        exist_style = conn.fetchone()
        if exist_style:
            return exist_style[0]
            
        conn.execute(sql_style, (updated_style_name,))
        style_id = conn.fetchone()[0]

    return style_id

def update_category(updated_category_name, gender_id,style_id,):
    sql_category = "INSERT INTO category(category_name,gender_id,style_id) VALUES(%s,%s,%s) RETURNING id;"
    with  con.cursor() as conn :
        conn.execute("SELECT * FROM category WHERE category_name = (%s)", (updated_category_name,))
        exist_category = conn.fetchone()
        if exist_category:
            return exist_category[0]
            
        conn.execute(sql_category, (updated_category_name, gender_id,style_id,))
        category_id = conn.fetchone()[0]

    return category_id

def update_color(color_name : str,):
    sql_color = "INSERT INTO color(color_name) VALUES(%s) RETURNING id;"
    with  con.cursor() as conn :
        conn.execute("SELECT * FROM color WHERE color_name = (%s)", (color_name,))
        exist_color = conn.fetchone()
        if exist_color:
            return exist_color[0]
            
        conn.execute(sql_color, (color_name,))
        color_id = conn.fetchone()[0]
        
    return color_id

def update_size(size : str,):
    sql_size = "INSERT INTO size(size) VALUES(%s) RETURNING id;"
    with  con.cursor() as conn :
        conn.execute("SELECT * FROM size WHERE size = (%s)", (size,))
        exist_size = conn.fetchone()
        if exist_size:
            return exist_size[0]
            
        conn.execute(sql_size, (size,))
        size_id = conn.fetchone()[0]
        
    return size_id

def update_stock_quantity(quantity : int,):
    sql_stock_quantity = "UPDATE stock_quantity SET quantity = %s,modified_at = %s RETURNING id;"
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
            
        gender_id = update_gender(gender_type)
            
        style_id = update_style(style_name)

        category_id = update_category(category_name,gender_id,style_id)
           
        conn.execute(sql_product, (category_id, name, description,))   
        product_id = conn.fetchone()[0]

    return product_id


@router.patch("/product/update_product/{product_id}")
async def update_product(product_id:int, Product : schemas._Product, Category : schemas._Category, Gender : schemas._Gender, Style : schemas._Style):

    sql_product = """UPDATE product SET 
    category_id = %s,
    name = %s,
    description = %s
    WHERE id = %s
    RETURNING id;"""

    with  con.cursor() as conn :
        try:
            conn.execute("SELECT * FROM product WHERE name = (%s)", (Product.name,))
            exist_product = conn.fetchone()
            if exist_product:
                raise HTTPException(status_code=400, detail="product already exists")

            gender_id = update_gender(Gender.gender_type)

            style_id = update_style(Style.style_name)

            category_id = update_category(Category.category_name,gender_id,style_id)

            conn.execute("SELECT * FROM product WHERE id = (%s)", (product_id,))
            exist_product = conn.fetchone()
            if exist_product:
                raise HTTPException(status_code=404, detail="product not found")

            conn.execute(sql_product, (category_id, Product.name, Product.description,product_id,))   
            product_id = conn.fetchone()[0]

            con.commit()
            print("product updated successefully")

        except Exception as e:
            con.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred while processing your request {e}",
            )


    return product_id
 
@router.patch("/product/update_product_item/{product_item_id}")
async def update_product_item(Product_item_id : int,
                              Product_item : schemas._Product_item, 
                              Product : schemas._Product,
                              Stock_quantity : schemas._Stock_quantity, 
                              Category : schemas._Category, 
                              Size : schemas._size, 
                              Color : schemas._Color , 
                              Style : schemas._Style, 
                              Gender : schemas._Gender):
    
    sql_product_item = """UPDATE product_item SET 
                        product_id = %s,
                        color_id = %s,
                        size_id = %s,
                        price = %s,
                        WHERE id = %s
                        RETURNING id;"""
    with  con.cursor() as conn :
        try:
            color_id = update_color(Color.color_name)
            size_id = update_size(Size.size)
            update_stock_quantity(Stock_quantity.quantity)
            Product_id = insert_product(Product.name, 
                                        Product.description, 
                                        Gender.gender_type, 
                                        Style.style_name, 
                                        Category.category_name,)
            

            conn.execute(sql_product_item, 
                         (Product_id, 
                          color_id, 
                          size_id, 
                          Product_item.price,
                          Product_item_id, 
                          ))
               
            Product_item_id = conn.fetchone()[0]
            
        except Exception as e:
            con.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred while processing your request {e}",
            )

        con.commit()
        return "product item updated successefully"