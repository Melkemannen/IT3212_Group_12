import pandas as pd

df = pd.read_csv('OnlineNewsPopularity.csv')

df.columns = df.columns.str.strip()

df.info()
#filtering the dataset (task 1, c)
filtered_df = df[(df['n_tokens_title'] == 0) | 
                 (df['n_tokens_content'] == 0) | 
                 (df['n_unique_tokens'] == 0)]

# Save the filtered DataFrame to a new CSV file
filtered_df.to_csv('filtered_file.csv', index=False)

# display the filtered DataFrame
print(filtered_df)

# find NULl values in data set
missing_values = df.isnull().sum()

if missing_values.any():
    print(f"Missing values in each column:\n{missing_values[missing_values > 0]}")
else:
    print("No missing values found in the dataset.")

# analyze unique values in categorical columns
categorical_columns = [
    'data_channel_is_lifestyle', 'data_channel_is_entertainment', 'data_channel_is_bus',
    'data_channel_is_socmed', 'data_channel_is_tech', 'data_channel_is_world', 
    'weekday_is_monday', 'weekday_is_tuesday', 'weekday_is_wednesday',
    'weekday_is_thursday', 'weekday_is_friday', 'weekday_is_saturday',
    'weekday_is_sunday', 'is_weekend'
]

for column in categorical_columns:
    unique_values = df[column].unique()
    print(f"Unique values in '{column}': {unique_values}")