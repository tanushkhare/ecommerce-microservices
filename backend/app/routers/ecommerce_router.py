from fastapi import APIRouter, HTTPException
from typing import List
from backend.app.schemas.ecommerce_schema import Product, CheckoutRequest, OrderResponse
from backend.app.services.ecommerce_service import store_service

router = APIRouter(prefix="/api/v1/orders", tags=["E-Commerce Microservices"])

@router.get("/products", response_model=List[Product])
async def list_products():
    return store_service.get_products()

@router.post("/checkout", response_model=OrderResponse)
async def checkout_order(payload: CheckoutRequest):
    try:
        order = await store_service.execute_checkout(payload.product_id, payload.quantity, payload.customer_email)
        return OrderResponse(**order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
