from fastapi import APIRouter, HTTPException
from app.schemas.store import ProductOrder
from app.services.store_service import get_inventory, process_order

router = APIRouter(prefix="/api", tags=["E-Commerce Microservice"])

@router.get("/products")
def list_products():
    return get_inventory()

@router.post("/orders")
def place_order(order: ProductOrder):
    result = process_order(order)
    if "error" in result:
        raise HTTPException(status_code=result["status"], detail=result["error"])
    return result