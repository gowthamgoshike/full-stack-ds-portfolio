import pandas as pd
import sklearn

data = {'Column A': [1, 2, 3], 'Column B': [4, 5, 6]}
df = pd.DataFrame(data)

print("SUCCESS! Your environment is ready.")
print(f"Pandas version: {pd.__version__}")
print(f"Scikit-Learn version: {sklearn.__version__}")
print("\nHere is your test DataFrame:")
print(df)