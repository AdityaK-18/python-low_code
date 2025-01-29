import streamlit as st
import requests
import os

# FastAPI URL (use environment variable or default to localhost)
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")

st.title("Product Management App")

# Sidebar menu
menu = st.sidebar.selectbox("Menu", ["View Products", "Add Product", "Delete Product"])

# View Products
if menu == "View Products":
    st.header("Product List")
    response = requests.get(f"{FASTAPI_URL}/products/")
    if response.status_code == 200:
        products = response.json()
        if products:
            for product in products:
                st.write(f"**ID**: {product['id']}, **Name**: {product['name']}, **Price**: ${product['price']}")
                st.write(f"Description: {product['description']}")
                st.write("---")
        else:
            st.write("No products available.")
    else:
        st.error("Failed to fetch products.")

# Add Product
elif menu == "Add Product":
    st.header("Add a New Product")
    product_id = st.number_input("Product ID", min_value=1, step=1)
    product_name = st.text_input("Product Name")
    product_description = st.text_area("Product Description")
    product_price = st.number_input("Product Price", min_value=0.0, step=0.01)

    if st.button("Add Product"):
        product_data = {
            "id": product_id,
            "name": product_name,
            "description": product_description,
            "price": product_price,
        }
        response = requests.post(f"{FASTAPI_URL}/products/", json=product_data)
        if response.status_code == 201:
            st.success("Product added successfully!")
        else:
            st.error(response.json().get("detail", "Failed to add product."))

# Delete Product
elif menu == "Delete Product":
    st.header("Delete a Product")
    product_id = st.number_input("Product ID to Delete", min_value=1, step=1)

    if st.button("Delete Product"):
        response = requests.delete(f"{FASTAPI_URL}/products/{product_id}")
        if response.status_code == 200:
            st.success("Product deleted successfully!")
        else:
            st.error("Failed to delete product.")
