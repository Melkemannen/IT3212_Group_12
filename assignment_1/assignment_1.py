import pandas as pd
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv('OnlineNewsPopularity.csv')

#print("Duplicate rows in the dataset: ")
#print(df.duplicated().sum())

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

#Self explanatory
weekday_columns = [
    'weekday_is_monday', 'weekday_is_tuesday', 'weekday_is_wednesday',
    'weekday_is_thursday', 'weekday_is_friday', 'weekday_is_saturday',
    'weekday_is_sunday'
]

#Filter for double checked days
filtered_df = df[df[weekday_columns].sum(axis=1) >= 2]

#Save to file
filtered_df.to_csv('filtered_days.csv', index=False)


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

## Task 4a
df = df.drop(columns=['url']) # drops the 'url' column

## Task 4b

#Identifies columns that are using 0-1 range
binary_columns = [col for col in df.columns if col.startswith('weekday_is') or col.startswith('data_channel_is')]

# Identifies columns that are NOT using 0-1 range except shares??
continuous_columns = [col for col in df.columns if col not in binary_columns and col != 'shares']

# Initialize Min-Max Scaler
scaler = MinMaxScaler()

# Apply Min-Max scaling to continuous columns
df[continuous_columns] = scaler.fit_transform(df[continuous_columns])

# Now the dataframe contains the scaled features
print(df.head())

# Saves the cleaned and transformed dataset to a new CSV file
df.to_csv('OnlineNewsPopularity_transformed.csv', index=False) # saves the cleaned dataset to a new CSV file