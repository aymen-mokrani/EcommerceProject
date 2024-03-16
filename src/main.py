import fastapi as _fastapi
from routers.product import insert_product, update_product, view_product, delete_product

app = _fastapi.FastAPI()

def include_routes(lst):
    for route in lst:
        app.include_router(route.router)

product_routes = [insert_product, update_product, view_product, delete_product]

include_routes(product_routes)

@app.get("/")
def read_home():
    return "Welcome to our store!"