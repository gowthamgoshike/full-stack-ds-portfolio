import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# --- STEP 1: SETUP CONNECTION ---
# Replace 'YourPassword' with your actual MySQL password
db_user = 'root'
db_password = 'Gowtham%40123'  # <--- UPDATE THIS!
db_host = 'localhost'
db_name = 'quickbite_analytics'

# Create the connection engine
connection_str = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}'
engine = create_engine(connection_str)
print("✅ Connection Engine Created Successfully!")

# --- STEP 2: EXTRACT DATA (SQL) ---
sql_query = """
SELECT 
    c.city,
    c.name as customer_name,
    o.amount,
    o.status
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.status = 'Delivered';
"""

print("⏳ Fetching data from MySQL...")
df = pd.read_sql(sql_query, engine)

# --- STEP 3: TRANSFORM DATA (Pandas) ---
print(f"Data Loaded: {len(df)} rows found.")

# Calculate Total Revenue per City
city_revenue = df.groupby('city')['amount'].sum().reset_index()
city_revenue = city_revenue.sort_values(by='amount', ascending=False)

print("\n--- Revenue Leaderboard ---")
print(city_revenue)

# --- STEP 4: VISUALIZE (Matplotlib/Seaborn) ---
plt.figure(figsize=(10, 6))
sns.set_theme(style="whitegrid")

# Create Bar Chart
barplot = sns.barplot(x='city', y='amount', data=city_revenue, palette='viridis')

# Add Labels
plt.title('Total Revenue by City (Real-Time SQL Data)', fontsize=16)
plt.xlabel('City', fontsize=12)
plt.ylabel('Revenue (₹)', fontsize=12)
plt.bar_label(barplot.containers[0], fmt='₹%.0f')

# Display the Chart
print("📊 Opening Visualization...")
plt.show()