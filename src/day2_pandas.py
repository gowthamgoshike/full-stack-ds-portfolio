import pandas as pd
import numpy as np
import time

def create_heavy_dataset(rows=1_000_000):
    """Creates a dataset that takes up memory."""
    print(f"Generating {rows} rows of data...")
    np.random.seed(42)
    data = {
        'age': np.random.randint(18, 90, size=rows),
        'salary': np.random.randint(30000, 150000, size=rows),
        'status': np.random.choice(['active', 'inactive', 'pending'], size=rows),
        'department': np.random.choice(['sales', 'eng', 'hr', 'marketing'], size=rows)
    }
    return pd.DataFrame(data)

def optimize_memory(df):
    """Reduces memory usage by converting string objects to categories and huge ints to small ints."""
    start_mem = df.memory_usage().sum() / 1024**2
    print(f"Memory before optimization: {start_mem:.2f} MB")

    # Optimization 1: Downcast numbers (int64 -> int8/16)
    # Age never exceeds 100, so we don't need 64 bits (which stores up to 9 quintillion)
    df['age'] = df['age'].astype('int8')
    df['salary'] = df['salary'].astype('int32')

    # Optimization 2: Categories
    # 'status' only has 3 unique values. Storing them as strings repeats text 1M times.
    # 'category' stores the text once and uses tiny integers in the rows.
    df['status'] = df['status'].astype('category')
    df['department'] = df['department'].astype('category')

    end_mem = df.memory_usage().sum() / 1024**2
    print(f"Memory after optimization: {end_mem:.2f} MB")
    print(f"Reduction: {100 * (start_mem - end_mem) / start_mem:.1f}%")
    return df

def method_chaining_example(df):
    """Demonstrates clean chaining."""
    print("\nRunning Method Chaining...")
    # Goal: Find average salary of active employees in 'eng' dept
    
    # The "Clean" Way
    result = (
        df
        .query("status == 'active'")
        .query("department == 'eng'")
        .groupby('department', observed=True)['salary']
        .mean()
    )
    print("Average Engineering Salary:", result.values[0])











if __name__ == "__main__":
    # 1. Generate Data
    df = create_heavy_dataset()
    
    # 2. Run Optimization
    df = optimize_memory(df)
    
    # 3. Run Analysis
    method_chaining_example(df)


