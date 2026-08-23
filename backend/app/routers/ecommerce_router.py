from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
import uuid

router = APIRouter(prefix="/api/v1/orders", tags=["E-Commerce Microservices Gateway"])

class CheckoutRequest(BaseModel):
    customer_id: str = Field(..., min_length=3)
    product_id: str
    product_name: str
    quantity: int = Field(..., ge=1, le=100)
    unit_price: float = Field(..., gt=0.0)

class CheckoutResponse(BaseModel):
    order_id: str
    payment_id: str
    customer_id: str
    product_name: str
    quantity: int
    total_price: float
    status: str
    traces: List[str]

@router.post("/checkout", response_model=CheckoutResponse)
async def process_checkout(payload: CheckoutRequest):
    total = round(payload.unit_price * payload.quantity, 2)
    order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    payment_id = f"PAY-{uuid.uuid4().hex[:8].upper()}"

    traces = [
        f"[Gateway API] Received checkout payload for customer {payload.customer_id}",
        f"[Inventory Service] Reserved {payload.quantity} unit(s) of {payload.product_id}",
        f"[Payment Service] Charged ${total:.2f} (TxID: {payment_id})",
        f"[Notification Service] Order receipt dispatched to customer queue"
    ]

    return CheckoutResponse(
        order_id=order_id,
        payment_id=payment_id,
        customer_id=payload.customer_id,
        product_name=payload.product_name,
        quantity=payload.quantity,
        total_price=total,
        status="CONFIRMED",
        traces=traces
    )