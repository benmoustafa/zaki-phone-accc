import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="📱 Phone Store Dashboard", layout="wide")

# Connect to DB
conn = sqlite3.connect("store.db")

# Load tables
products_df = pd.read_sql("SELECT * FROM Products", conn)
sales_df = pd.read_sql("SELECT * FROM DailySales", conn)

st.title("📊 Phone Store Management")

# Tabs
tab1, tab2, tab3 = st.tabs(["🔍 Search Product", "🛒 Record Sale", "📈 Reports"])

# --- Search Product ---
with tab1:
    search = st.text_input("Enter Product ID or Name")
    if search:
        results = products_df[
            products_df["ProductID"].str.contains(search, case=False, na=False) |
            products_df["Model"].str.contains(search, case=False, na=False) |
            products_df["Brand"].str.contains(search, case=False, na=False)
        ]
        if not results.empty:
            st.dataframe(results)
        else:
            st.warning("No product found.")

# --- Record Sale ---
with tab2:
    with st.form("sale_form"):
        date = st.date_input("Date")
        product = st.selectbox("Select Product", products_df["Model"])
        qty = st.number_input("Quantity Sold", min_value=1, step=1)
        seller = st.text_input("Seller Name")
        submit = st.form_submit_button("Save Sale")

        if submit:
            product_id = products_df[products_df["Model"] == product]["ProductID"].iloc[0]
            new_sale = pd.DataFrame([[date, product_id, qty, seller]], 
                                    columns=["Date", "ProductID", "QuantitySold", "SellerName"])
            new_sale.to_sql("DailySales", conn, if_exists="append", index=False)
            st.success("✅ Sale recorded!")

# --- Reports ---
with tab3:
    revenue = pd.read_sql("""
        SELECT s.Date, p.Brand, p.Model, SUM(s.[Quantity Sold] * p.Price) as Revenue
        FROM DailySales s
        JOIN Products p ON s.ProductID = p.ProductID
        GROUP BY s.Date, p.Brand, p.Model
        ORDER BY s.Date DESC
    """, conn)

    st.subheader("📅 Daily Revenue")
    st.dataframe(revenue)


