from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Product(BaseModel):
    product_id: int
    name: str
    price: float
    stock: int
    category: str

class CheckoutRequest(BaseModel):
    product_id: int = Field(..., description="Target inventory product ID")
    quantity: int = Field(..., ge=1, le=50, description="Order quantity")
    customer_email: Optional[str] = Field(default="dev@domain.com")

class OrderResponse(BaseModel):
    order_id: str
    product_id: int
    product_name: str
    quantity: int
    total_amount: float
    status: str
    remaining_stock: int
    timestamp: str
