import asyncio
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

class InventoryStoreService:
    def __init__(self):
        self.inventory: Dict[int, Dict[str, Any]] = {
            101: {"product_id": 101, "name": "Enterprise Cloud Node", "price": 499.00, "stock": 25, "category": "Compute"},
            102: {"product_id": 102, "name": "AI Accelerator GPU", "price": 1299.00, "stock": 10, "category": "Hardware"},
            103: {"product_id": 103, "name": "Managed Redis Cluster", "price": 199.00, "stock": 40, "category": "Database"},
            104: {"product_id": 104, "name": "Zero-Trust Security Key", "price": 49.00, "stock": 100, "category": "Security"}
        }
        self.orders: List[Dict[str, Any]] = []
        self._locks: Dict[int, asyncio.Lock] = {}

    def get_products(self) -> List[Dict[str, Any]]:
        return list(self.inventory.values())

    async def execute_checkout(self, product_id: int, quantity: int, email: str) -> Dict[str, Any]:
        # Guard inventory mutation with per-product mutex lock to eliminate race conditions
        lock = self._locks.setdefault(product_id, asyncio.Lock())
        async with lock:
            product = self.inventory.get(product_id)
            if not product:
                raise ValueError(f"Product with ID {product_id} not found in inventory catalog.")
            
            if product["stock"] < quantity:
                raise ValueError(f"Insufficient stock for {product['name']}. Available: {product['stock']}, Requested: {quantity}")

            # Atomic stock decrement
            product["stock"] -= quantity
            total_price = round(product["price"] * quantity, 2)
            now = datetime.now(timezone.utc).isoformat()
            order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"

            order_record = {
                "order_id": order_id,
                "product_id": product_id,
                "product_name": product["name"],
                "quantity": quantity,
                "total_amount": total_price,
                "status": "CONFIRMED",
                "remaining_stock": product["stock"],
                "timestamp": now
            }
            self.orders.append(order_record)
            return order_record

store_service = InventoryStoreService()
