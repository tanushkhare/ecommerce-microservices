inventory_db = [
    {"product_id": 1, "name": "Wireless Mechanical Keyboard", "price": 89.99, "stock": 15},
    {"product_id": 2, "name": "Ergonomic Vertical Mouse", "price": 45.50, "stock": 30},
    {"product_id": 3, "name": "Ultra-Wide 4K Monitor", "price": 399.99, "stock": 5}
]

orders_db = []

def get_inventory():
    return inventory_db

def process_order(order_data):
    product = next((p for p in inventory_db if p["product_id"] == order_data.product_id), None)
    if not product:
        return {"error": "Product not found", "status": 404}
    if product["stock"] < order_data.quantity:
        return {"error": "Insufficient stock available", "status": 400}
    
    product["stock"] -= order_data.quantity
    order_record = {
        "order_id": len(orders_db) + 1,
        "product_name": product["name"],
        "quantity": order_data.quantity,
        "total_price": round(product["price"] * order_data.quantity, 2),
        "customer_email": order_data.customer_email,
        "status": "Confirmed"
    }
    orders_db.append(order_record)
    return order_record