import mysql.connector
import os
from dotenv import load_dotenv

# 1. LOAD SECRETS
# This looks for the .env file to get your DB_PASSWORD
load_dotenv()

def create_and_seed_database():
    print("🔌 Connecting to MySQL Server...")
    
    # Connect to the Server (not the specific DB yet)
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD')
        )
        cursor = conn.cursor()
        print("✅ Connected to Server.")
    except mysql.connector.Error as err:
        print(f"❌ Error connecting to MySQL: {err}")
        print("💡 Hint: Check your .env file and make sure XAMPP/MySQL Workbench is running.")
        return

    # 2. CREATE DATABASE (The Container)
    cursor.execute("CREATE DATABASE IF NOT EXISTS retail_db")
    cursor.execute("USE retail_db")
    print("✅ Database 'retail_db' selected.")

    # 3. CREATE TABLE (The Schema)
    # We drop it first to ensure a fresh start every time you run this script
    cursor.execute("DROP TABLE IF EXISTS transactions")
    
    cursor.execute("""
        CREATE TABLE transactions (
            txn_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT,
            amount DECIMAL(10,2),
            category VARCHAR(50),
            is_returned BOOLEAN,
            txn_date DATE
        )
    """)
    print("✅ Table 'transactions' created.")

    # 4. SEED SMART DATA (The Logic)
    # We need specific patterns for your Data Science engine to find:
    # Pattern A: Electronics are expensive and have high returns.
    # Pattern B: Fashion is cheap and has low returns.
    # Pattern C: A few massive outliers.
    
    print("🌱 Seeding data...")
    sql = "INSERT INTO transactions (customer_id, amount, category, is_returned, txn_date) VALUES (%s, %s, %s, %s, %s)"
    data = []

    # -- Generate 100 rows of 'Normal' Data --
    for i in range(100):
        # Case 1: Fashion (Low Risk)
        # Price ~ $50, Return Rate ~ 5%
        data.append((i, 50.00, 'Fashion', 0, '2025-06-01')) 
        
        # Case 2: Electronics (High Risk)
        # Price ~ $1200, Return Rate ~ 50% (High correlation for Bayes)
        data.append((i, 1200.00, 'Electronics', 1, '2025-06-02')) 
        data.append((i, 1150.00, 'Electronics', 0, '2025-06-02')) # Not returned

    # -- Inject Outliers (For IQR Detection) --
    # The "Whale" Purchase
    data.append((999, 50000.00, 'Electronics', 0, '2025-06-05')) 
    
    # The "Glitch" Purchase (Too low)
    data.append((888, 1.50, 'Fashion', 0, '2025-06-06'))

    # 5. INSERT AND SAVE
    cursor.executemany(sql, data)
    conn.commit()
    print(f"✅ Success! {len(data)} rows inserted.")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_and_seed_database()