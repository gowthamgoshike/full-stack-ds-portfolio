import pandas as pd
from scipy import stats
from .database import DatabaseConnector

class DataScienceEngine:
    def __init__(self):
        self.db = DatabaseConnector()

    def get_clean_data(self):
        """Fetches raw data from MySQL"""
        return self.db.run_query("SELECT * FROM transactions")

    def detect_outliers(self, df, column='amount'):
        """
        Calculates IQR Outliers.
        Returns: Processed DataFrame, Lower Fence, Upper Fence
        """
        if df.empty:
            return df, 0, 0

        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_fence = Q1 - (1.5 * IQR)
        upper_fence = Q3 + (1.5 * IQR)

        # Mark rows as True/False
        df['is_outlier'] = (df[column] < lower_fence) | (df[column] > upper_fence)
        return df, lower_fence, upper_fence

    def calculate_bayes_return_prob(self, category):
        """
        Calculates P(Return | Category) using Bayes' Theorem
        """
        df = self.get_clean_data()
        
        if df.empty: return 0.0

        # 1. Priors
        p_category = len(df[df['category'] == category]) / len(df)
        p_return = len(df[df['is_returned'] == 1]) / len(df)
        
        # 2. Likelihood: P(Category | Return)
        returned_items = df[df['is_returned'] == 1]
        if len(returned_items) == 0: return 0.0
        
        p_cat_given_return = len(returned_items[returned_items['category'] == category]) / len(returned_items)
        
        # 3. Bayes Formula
        if p_category == 0: return 0.0
        prob = (p_cat_given_return * p_return) / p_category
        return prob