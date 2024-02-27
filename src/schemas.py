from pydantic import BaseModel, field_validator, Field, EmailStr
import re
from datetime import datetime
from uuid import UUID, uuid4 as uuid

class _Useer(BaseModel):
    first_name : str = Field(min_length=2, max_length=50)
    last_name : str = Field(min_length=2, max_length=50)
    email : EmailStr
    phone : str 
    Address_id : int
    password : str = Field(min_length=8, max_length=50)

    @field_validator("phone")
    def validate_phone_number(cls, v):
        if not re.match(r'^\+(?:[0-9] ?){6,14}[0-9]$', v):
            raise ValueError('Invalid phone number format')
        return v
  
class _Address(BaseModel):
    
    unit_number : str = Field(min_length=2, max_length=50)
    street_number : str = Field(min_length=2, max_length=50)
    address_line : str = Field(min_length=2, max_length=200)
    city : str = Field(min_length=2, max_length=50)
    region : str = Field(min_length=2, max_length=50)
    postal_code : str = Field(min_length=2, max_length=50)
    country_id : int

class _Style(BaseModel):
    
    style_name : str = Field(min_length=2, max_length=50)
    
class _Gender(BaseModel):
    
    gender_type : str = Field(min_length=2, max_length=50)
    
class _Category(BaseModel):
    
    category_name : str = Field(min_length=2, max_length=50)
    gender_id : int
    style_id : int

class _Product(BaseModel):
    category_id : int
    name : str = Field(min_length=2, max_length=50)
    description : str = Field(min_length=2, max_length=500)  


class _Color(BaseModel):
    color_name : str = Field(min_length=2, max_length=50)
     
class _size(BaseModel):
    size : str = Field(min_length=1, max_length=10)

class _Stock_quantity(BaseModel):
    quantity : int = Field(max_length=100)
    created_at : datetime = Field(default_factory=datetime.now)
    modified_at : datetime 
    deleted_at : datetime 

class _Product_item(BaseModel):
    product_id : int
    color_id : int
    size_id : int
    sku : UUID = Field(default_factory = lambda: uuid())
    price : float = Field(gt=0)
    stock_quantity_id : int
    
class _Order_line(BaseModel):
    product_item_id : int
    order_id : int
    qty : int = Field(gt=0)
    price : float = Field(gt=0)

class _Shipping_method(BaseModel):
    method : str = Field(min_length=2, max_length=50)
    price : float = Field(gt=0)

class _Order_status(BaseModel):
    status : str = Field(min_length=2, max_length=50)

class _Shop_order(BaseModel):
    user_id : int
    order_date : datetime
    payment_id : int
    shipping_address_id : int
    shipping_method_id : int
    order_total : float =Field(gr=0)
    order_status_id : int

class _Payment_type(BaseModel):
    type : str = Field(min_length=1,max_length=100)

class _Payment(BaseModel):
    user_id : int
    payment_type_id : int
    provider : str = Field(min_length=1, max_length=100)
    accout_number : str = Field(min_length=1, max_length=50)

class _Shopping_cart_item(BaseModel):
    cart_id : int
    product_id : int
    qty : int = Field(gt=0)

class _Shopping_cart(BaseModel):
    user_id : int

class _Country(BaseModel):
    country_name : str = Field(min_length=2, max_length=50)