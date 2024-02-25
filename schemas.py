import pydantic as _pydantic

class _BaseOrder_status(_pydantic.BaseModel):
    status : str

class Order_status(_BaseOrder_status):
    id : int

    class Config:
        from_attributes=True

class CreateOrder_status(_BaseOrder_status):
    pass