import pydantic as _pydantic

class _BaseOrder_status(_pydantic.BaseModel):
    status : str

class Order_status(_BaseOrder_status):
    id : int

    class Config:
        from_attributes=True


class CreateOrder_status(_BaseOrder_status):
    pass

class _BaseProduct(_pydantic.BaseModel):
    category_id : int
    name : str
    description : str    

class Product(_BaseProduct):
    id : int

    class Config:
        from_attributes=True

class CreateProduct(_BaseProduct):
    pass

class _BaseAddress(_pydantic.BaseModel):
    
    unit_number : str
    street_number : str
    address_line : str
    city : str
    region : str
    postal_code : str
    country_id : int

class Address(_BaseAddress):
    id : int

    class Config:
        from_attributes=True

class CreateAddress(_BaseProduct):
    pass