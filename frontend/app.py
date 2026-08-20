import streamlit as st
import requests

st.title("🛒 E-Commerce Microservices Storefront")
st.write("Browse live product inventory and place orders securely against the decoupled microservice backend.")

st.subheader("📦 Current Product Catalog")
try:
    res = requests.get("http://127.0.0.1:8000/api/products")
    if res.status_code == 200:
        products = res.json()
        for p in products:
            st.info(f"**ID: {p['product_id']} | {p['name']}** \n\n Price: ${p['price']} | In Stock: **{p['stock']}**")
    else:
        st.error("Could not fetch product catalog.")
except Exception as e:
    st.error(f"Connection failed: {e}")

st.divider()

st.subheader("🛍️ Place a New Order")
prod_id = st.number_input("Product ID", min_value=1, step=1)
qty = st.number_input("Quantity", min_value=1, step=1)
email = st.text_input("Customer Email")

if st.button("Submit Order"):
    if email.strip():
        try:
            payload = {"product_id": int(prod_id), "quantity": int(qty), "customer_email": email}
            response = requests.post("http://127.0.0.1:8000/api/orders", json=payload)
            if response.status_code == 200:
                data = response.json()
                st.success(f"Order #{data['order_id']} placed successfully for {data['product_name']}! Total: ${data['total_price']}")
            else:
                err = response.json()
                st.error(f"Order failed: {err.get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"API communication error: {e}")
    else:
        st.warning("Please provide a valid customer email.")