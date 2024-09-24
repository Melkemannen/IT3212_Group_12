import pandas as pd

df = pd.read_csv('OnlineNewsPopularity.csv')

df.info()

missing_values = df.isnull().sum()

if missing_values.any():
    print(f"Missing values in each column:\n{missing_values[missing_values > 0]}")
else:
    print("No missing values found in the dataset.")
