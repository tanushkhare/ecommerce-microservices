from pydantic import BaseModel

class ProductOrder(BaseModel):
    product_id: int
    quantity: int
    customer_email: str