import streamlit as st
import requests
import pandas as pd

# API endpoint
API_URL = "http://127.0.0.1:8000/products/"

st.title("Product Management System")

# Add Product Form
st.sidebar.header("Add New Product")
product_id = st.sidebar.number_input("Product ID", min_value=1, step=1)
product_name = st.sidebar.text_input("Product Name")
product_description = st.sidebar.text_area("Product Description")
product_price = st.sidebar.number_input("Product Price", min_value=0.0, step=0.01)

if st.sidebar.button("Add Product"):
    product_data = {
        "id": product_id,
        "name": product_name,
        "description": product_description,
        "price": product_price,
    }
    response = requests.post(API_URL, json=product_data)
    if response.status_code == 200:
        st.sidebar.success("Product added successfully!")
    else:
        st.sidebar.error(f"Error: {response.json().get('detail', 'Unknown error')}")

# Bulk Upload Products
st.sidebar.header("Bulk Upload Products")
bulk_upload = st.sidebar.file_uploader("Upload JSON file", type=["json"])
if bulk_upload:
    try:
        # Read the uploaded file
        products = pd.read_json(bulk_upload).to_dict(orient="records")
        response = requests.post(f"{API_URL}bulk/", json=products)
        if response.status_code == 200:
            st.sidebar.success(response.json().get("message", "Products added successfully!"))
        else:
            st.sidebar.error(f"Error: {response.json().get('detail', 'Unknown error')}")
    except Exception as e:
        st.sidebar.error(f"Invalid JSON file: {e}")

# Display Products
st.header("Product List")
response = requests.get(API_URL)
if response.status_code == 200:
    products = response.json()
    if products:
        df = pd.DataFrame(products)
        st.dataframe(df)

        # Update Product
        st.header("Update a Product")
        update_id = st.number_input("Enter Product ID to Update", min_value=1, step=1)
        updated_name = st.text_input("Updated Name")
        updated_description = st.text_area("Updated Description")
        updated_price = st.number_input("Updated Price", min_value=0.0, step=0.01)
        if st.button("Update Product"):
            updated_data = {
                "id": update_id,
                "name": updated_name,
                "description": updated_description,
                "price": updated_price,
            }
            update_response = requests.put(f"{API_URL}{update_id}", json=updated_data)
            if update_response.status_code == 200:
                st.success("Product updated successfully!")
            else:
                st.error(f"Error: {update_response.json().get('detail', 'Unknown error')}")

        # Delete Product
        st.header("Delete a Product")
        delete_id = st.number_input("Enter Product ID to Delete", min_value=1, step=1)
        if st.button("Delete Product"):
            delete_response = requests.delete(f"{API_URL}{delete_id}")
            if delete_response.status_code == 200:
                st.success("Product deleted successfully!")
            else:
                st.error(f"Error: {delete_response.json().get('detail', 'Unknown error')}")
    else:
        st.write("No products available.")
else:
    st.error(f"Error fetching products: {response.status_code}")
