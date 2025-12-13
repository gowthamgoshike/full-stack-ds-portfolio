import pandas as pd

class DataCleaner:
    def __init__(self, df):
        # We create a copy so we don't mess up the original dataframe
        self.df = df.copy()

    def fix_columns(self):
        """Converts columns to snake_case"""
        self.df.columns = [x.lower().replace(' ', '_') for x in self.df.columns]
        return self

    def handle_missing_values(self, strategy='mean'):
        """Fills numerical missing values based on strategy"""
        for col in self.df.select_dtypes(include=['number']):
            if strategy == 'mean':
                self.df[col] = self.df[col].fillna(self.df[col].mean())
            elif strategy == 'zero':
                self.df[col] = self.df[col].fillna(0)
        return self

    def remove_duplicates(self):
        self.df = self.df.drop_duplicates()
        return self

    def get_clean_data(self):
        return self.df