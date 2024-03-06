from fastapi import APIRouter,HTTPException
from main import app
from database import init_connection
import schemas

con=init_connection()
router = APIRouter()

def insert_gender(gender_type):
    sql_gender = "INSERT INTO gender(gender_type) VALUES(%s);"
    with  con.cursor() as conn :
        conn.execute("SELECT * FROM gender WHERE gender_type = (%s)", (gender_type,))
        exist_gender = conn.fetchone()
        if exist_gender:
            return exist_gender
            
        conn.execute(sql_gender, (gender_type,))
        gender_id = conn.lastrowid()

    return gender_id

def insert_style(style_name):
    sql_style = "INSERT INTO style(style_name) VALUES(%s);"
    with  con.cursor() as conn :
        conn.execute("SELECT * FROM style WHERE style_name = (%s)", (style_name,))
        exist_style = conn.fetchone()
        if exist_style:
            return exist_style
            
        conn.execute(sql_style, (style_name,))
        style_id = conn.lastrowid()

    return style_id

def insert_category(category_name, gender_id,style_id,):
    sql_category = "INSERT INTO category(category_name,gender_id,style_id) VALUES(%s,%s,%s);"
    with  con.cursor() as conn :
        conn.execute("SELECT * FROM category WHERE category_name = (%s)", (category_name,))
        exist_category = conn.fetchone()
        if exist_category:
            return exist_category
            
        conn.execute(sql_category, (category_name, gender_id,style_id,))
        category_id = conn.lastrowid()

    return category_id


@router.post("/product/add")
async def create_product(Product : schemas._Product, Category : schemas._Category, Gender : schemas._Gender, Style : schemas._Style):

    sql_product = "INSERT INTO product(category_id,name,description) VALUES(%s,%s);"

    with  con.cursor() as conn :
        try:
            conn.execute("SELECT * FROM product WHERE name = (%s)", (Product.name,))
            exist_product = conn.fetchone()
            if exist_product:
                raise HTTPException(status_code=400, detail="product already exists")

            gender_id = insert_gender(Gender.gender_type)

            style_id = insert_style(Style.style_name)

            category_id = insert_category(Category.category_name,gender_id,style_id)

            conn.execute(sql_product, (category_id, Product.name, Product.description,))   
            product_id = conn.fetchone()

            con.commit()
            print("product added successefully")

        except Exception as e:
            con.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred while processing your request {e}",
            )


    return product_id
 

@app.get("/api/product")
async def get_products():
    
    with con.cursor() as conn :
        
        conn.execute("SELECT * FROM product;")
        products = conn.fetchall()
    
        
    return products