import mysql.connector
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnector:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD')
        self.database = 'retail_db' # We hardcode this since setup_db.py created it
        self.conn = None

    def connect(self):
        """Establishes connection to the specific retail_db"""
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except mysql.connector.Error as err:
            print(f"❌ DB Connection Error: {err}")
            raise

    def run_query(self, query):
        """Runs a SELECT query and returns a Pandas DataFrame"""
        if not self.conn or not self.conn.is_connected():
            self.connect()
        
        try:
            return pd.read_sql(query, self.conn)
        except Exception as e:
            print(f"Query Failed: {e}")
            return pd.DataFrame() # Return empty DF on fail