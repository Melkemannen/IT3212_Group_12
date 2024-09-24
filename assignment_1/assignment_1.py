import pandas as pd

df = pd.read_csv('OnlineNewsPopularity.csv')

df.info()
#filtering the dataset (task 1, c)
filtered_df = df[(df['n_tokens_title'] == 0) | 
                 (df['n_tokens_content'] == 0) | 
                 (df['n_unique_tokens'] == 0)]

# Save the filtered DataFrame to a new CSV file
filtered_df.to_csv('filtered_file.csv', index=False)

# display the filtered DataFrame
print(filtered_df)

missing_values = df.isnull().sum()

if missing_values.any():
    print(f"Missing values in each column:\n{missing_values[missing_values > 0]}")
else:
    print("No missing values found in the dataset.")
