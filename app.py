import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# --- Google Sheets Setup ---
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPE)
client = gspread.authorize(creds)

SHEET_ID1 = "174mvcqlIoM7gQd2Mbxz6UG5i_X9A4ZX1MKkoK1rwh08"  # Replace with your Google Sheet ID
SHEET_ID2 = "1oVeW7FKF2QEskFlJqQEN8sUD6CvS472m6cTQEEE4wBs"
# Load both datasets
products_ws = client.open_by_key(SHEET_ID1).worksheet("Sheet1")
sales_ws = client.open_by_key(SHEET_ID2).worksheet("Sheet1")

# Convert to DataFrames
products_df = pd.DataFrame(products_ws.get_all_records())
sales_df = pd.DataFrame(sales_ws.get_all_records())

# --- Streamlit UI ---
st.title("📊 zaki phone Manager")

tab1, tab2 = st.tabs(["📦 Products", "💰 Sales"])

# --- Products Tab ---
with tab1:
    st.subheader("Product List")
    st.dataframe(products_df)

    with st.form("add_product"):
        brand = st.text_input("Brand")
        model = st.text_input("Model")
        price = st.number_input("Price", min_value=0.0, format="%.2f")
        stock = st.number_input("Stock Quantity", min_value=0, step=1)
        submit = st.form_submit_button("➕ Add Product")

        if submit:
            products_ws.append_row([brand, model, price, stock])
            st.success(f"✅ Added {brand} {model}!")

# --- Sales Tab ---
with tab2:
    st.subheader("Sales Records")
    st.dataframe(sales_df)

    with st.form("add_sale"):
        date = st.date_input("Date")
        product = st.selectbox("Product", products_df["Model"] if not products_df.empty else [])
        qty = st.number_input("Quantity Sold", min_value=1, step=1)
        submit_sale = st.form_submit_button("➕ Add Sale")

        if submit_sale:
            sales_ws.append_row([str(date), product, qty])
            st.success(f"✅ Added sale: {qty} x {product} on {date}")
