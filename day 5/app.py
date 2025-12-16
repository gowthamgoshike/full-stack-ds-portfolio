import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="QuickBite Dashboard", layout="wide")

# --- 1. SETUP DATABASE CONNECTION (The "Backend") ---
# (Cache this function so we don't reconnect every time we click a button)
@st.cache_resource
def get_connection():
    db_user = 'root'
    # UPDATE YOUR PASSWORD HERE
    raw_password = 'Gowtham@123' 
    db_password = quote_plus(raw_password)
    db_host = 'localhost'
    db_name = 'quickbite_analytics'
    
    connection_str = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}'
    return create_engine(connection_str)

engine = get_connection()

# --- 2. FETCH DATA (The "Data Layer") ---
@st.cache_data
def load_data():
    query = """
    SELECT 
        c.city,
        c.name as customer_name,
        r.name as restaurant_name,
        o.amount,
        o.status,
        o.order_date
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN restaurants r ON o.restaurant_id = r.restaurant_id
    """
    return pd.read_sql(query, engine)

df = load_data()

# --- 3. SIDEBAR FILTERS (The "Frontend") ---
st.sidebar.header("Filter Options")

# City Filter
available_cities = df['city'].unique().tolist()
selected_cities = st.sidebar.multiselect('Select City', available_cities, default=available_cities)

# Apply Filter
filtered_df = df[df['city'].isin(selected_cities)]

# --- 4. MAIN DASHBOARD UI ---
st.title("🍔 QuickBite Analytics Dashboard")
st.markdown("Real-time view of food delivery performance.")

# KPI Row (Key Performance Indicators)
col1, col2, col3 = st.columns(3)
with col1:
    total_revenue = filtered_df[filtered_df['status'] == 'Delivered']['amount'].sum()
    st.metric("Total Revenue", f"₹{total_revenue:,.0f}")
with col2:
    
    total_orders = len(filtered_df)
    st.metric("Total Orders", total_orders)
with col3:
    avg_order = filtered_df['amount'].mean()
    st.metric("Avg Order Value", f"₹{avg_order:.0f}")

st.divider()

# Charts Row
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Revenue by City")
    # Group data for the chart
    city_data = filtered_df.groupby('city')['amount'].sum().reset_index()
    
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    sns.barplot(x='city', y='amount', data=city_data, palette='viridis', ax=ax1)
    ax1.set_ylabel("Revenue (₹)")
    st.pyplot(fig1)

with col_chart2:
    st.subheader("Order Status Distribution")
    status_counts = filtered_df['status'].value_counts()
    
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', colors=['#66b3ff','#ff9999'])
    st.pyplot(fig2)

# Raw Data Table (at the bottom)
with st.expander("View Raw Data"):
    st.dataframe(filtered_df)