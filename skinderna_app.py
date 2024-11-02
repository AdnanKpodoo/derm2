import json
import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie

# Load the Lottie animation file
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_skincare = load_lottiefile(".streamlit/skincare.json")

# URLs for Google Sheets CSV

PRODUCTS_URL = "https://docs.google.com/spreadsheets/d/1EeVOvxei4R1_y1g_ZoKp87CDb0LaLZmggIyeEUGZeuU/export?format=csv&gid=0"
BRANDS_URL = "https://docs.google.com/spreadsheets/d/1EeVOvxei4R1_y1g_ZoKp87CDb0LaLZmggIyeEUGZeuU/export?format=csv&gid=1366110017"  # Replace with actual gid for brands sheet

# Read data from the Google Sheets
products_df = pd.read_csv(PRODUCTS_URL)
brands_df = pd.read_csv(BRANDS_URL)

# Function to fetch products based on skin type from the 'products' DataFrame and 'brands' DataFrame
def get_products_from_sheets(products_df, brands_df, skin_type):
    products = []

    # Map brand IDs to names from the 'brands' DataFrame
    brand_map = {brand['brand_id']: brand['brand_name'] for _, brand in brands_df.iterrows()}

    # Filter products by skin type
    for _, product in products_df.iterrows():
        if product['skin_type'] == skin_type or (product['skin_type_two'] == skin_type and product['skin_type'] != skin_type):
            brand_name = brand_map.get(product['brand_id'], "Unknown Brand")
            products.append({
                "product_name": product['product_name'],
                "brand_name": brand_name,
                "category": product['category'],
                "description": product['description'],
                "price": product['price'],
                "skin_type": product['skin_type'],
                "skin_type_two": product['skin_type_two']
            })
    return products

# Streamlit Application
st.title('DermaDossier')
st.subheader('Start Your Search for a Basic Effective Routine!')

# Display the Lottie animation
st_lottie(
    lottie_skincare,
    speed=1,
    reverse=False,
    loop=True,
    quality="low",
    height=500,
    width=300
)

# Sidebar for selecting a skin type
st.subheader("Select Skin Type")
skin_type = st.selectbox("Options", ("Oily", "Dry", "Normal", "Combination", "Acne-Prone", "Sensitive", "All"))

# Display products based on selected skin type
if skin_type:
    st.subheader(f"Products For {skin_type} Skin")

    products = get_products_from_sheets(products_df, brands_df, skin_type)

    if products:
        for product in products:
            st.write(f"**Product Name**: {product['product_name']}")
            st.write(f"**Brand**: {product['brand_name']}")
            st.write(f"**Category**: {product['category']}")
            st.write(f"**Description**: {product['description']}")
            st.write(f"**Price**: ${product['price']:.2f}")
            st.write(f"**Skin Type**: {product['skin_type']}, {product['skin_type_two']}")
            st.write("---")
    else:
        st.write("No products found for the selected skin type.")
