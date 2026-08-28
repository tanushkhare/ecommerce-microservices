import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="E-Commerce Microservices Hub", layout="wide")

st.title("🛒 Distributed E-Commerce Microservices Engine")
st.markdown("Atomic checkout pipelines, concurrency-guarded inventory mutations, and order state management.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Inventory Catalog")
    try:
        res = requests.get("http://localhost:8000/api/v1/orders/products", timeout=4)
        if res.status_code == 200:
            products = res.json()
        else:
            products = [
                {"product_id": 101, "name": "Enterprise Cloud Node", "price": 499.00, "stock": 25, "category": "Compute"},
                {"product_id": 102, "name": "AI Accelerator GPU", "price": 1299.00, "stock": 10, "category": "Hardware"}
            ]
    except Exception:
        products = [
            {"product_id": 101, "name": "Enterprise Cloud Node", "price": 499.00, "stock": 25, "category": "Compute"},
            {"product_id": 102, "name": "AI Accelerator GPU", "price": 1299.00, "stock": 10, "category": "Hardware"}
        ]
    
    st.dataframe(pd.DataFrame(products), use_container_width=True)
    
    st.subheader("Checkout Pipeline")
    prod_options = {f"{p['name']} (${p['price']} | Stock: {p['stock']})": p['product_id'] for p in products}
    selected_label = st.selectbox("Select Product", list(prod_options.keys()))
    target_pid = prod_options[selected_label]
    qty = st.number_input("Quantity", min_value=1, max_value=20, value=1)
    
    if st.button("Dispatch Atomic Checkout", type="primary"):
        with st.spinner("Acquiring resource lock and executing transactional decrement..."):
            try:
                checkout_res = requests.post(
                    "http://localhost:8000/api/v1/orders/checkout",
                    json={"product_id": target_pid, "quantity": qty},
                    timeout=5
                )
                if checkout_res.status_code == 200:
                    st.session_state["p09_order"] = checkout_res.json()
                    st.success("Order Placed Successfully!")
                else:
                    st.error(f"Order Rejected: {checkout_res.json().get('detail', checkout_res.text)}")
            except Exception:
                st.warning("Backend offline. Simulating atomic transaction.")
                st.session_state["p09_order"] = {
                    "order_id": "ORD-SIM998",
                    "product_id": target_pid,
                    "product_name": selected_label.split(" (")[0],
                    "quantity": qty,
                    "total_amount": 499.00 * qty,
                    "status": "CONFIRMED",
                    "remaining_stock": 24,
                    "timestamp": "2026-08-28T07:15:00Z"
                }

with col2:
    if "p09_order" in st.session_state:
        order = st.session_state["p09_order"]
        st.subheader("Order Confirmation & Telemetry")
        
        m1, m2 = st.columns(2)
        m1.metric("Order ID", order["order_id"])
        m2.metric("Total Billed", f"${order['total_amount']:,.2f}", delta=f"Status: {order['status']}")
        
        st.markdown(f"**Item:** `{order['product_name']}` (Qty: {order['quantity']})")
        st.markdown(f"**Updated Inventory Level:** `{order['remaining_stock']}` units remaining")
