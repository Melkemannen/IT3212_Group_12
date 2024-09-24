import pandas as pd
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv('OnlineNewsPopularity.csv')

#print("Duplicate rows in the dataset: ")
#print(df.duplicated().sum())

df.columns = df.columns.str.strip()

df.info()
#Data cleaning TASK 2
filtered_df_tokens = df[(df['n_tokens_title'] == 0) | 
                 (df['n_tokens_content'] == 0) | 
                 (df['n_unique_tokens'] == 0)]

df_cleaned = df.drop(filtered_df_tokens.index)
df_cleaned.to_csv('cleaned_tokens.csv', index=False)

# Drop kw_min_min as -1 percentage is almost 60%
df_cleaned = df_cleaned.drop(columns=['kw_min_min'])

# Impute -1 to mean value in select columns
for column in ['kw_avg_min', 'kw_min_avg']:
    mean = df_cleaned[column][df_cleaned[column] != -1].mean()
    # Print percentage that is -1 befor imputing
    count = (df_cleaned[column] == -1).sum()
    total = df_cleaned[column].count()
    print((count/total) * 100)
    # Impute -1 values to mean
    df_cleaned[column] = df[column].replace(-1, mean)
    # Print after imputing
    count = (df_cleaned[column] == -1).sum()
    print((count/total) * 100)
    
# Save the filtered DataFrame to a new CSV file
filtered_df_tokens.to_csv('filtered_file.csv', index=False)

#Perform IQR based outlier detection on filtered_file.csv
#Detect on tokens first, then on shares
Q1_tokens = df_cleaned['n_tokens_content'].quantile(0.25)
Q3_tokens = df_cleaned['n_tokens_content'].quantile(0.75)
IQR_tokens = Q3_tokens - Q1_tokens
print(f"TOKENS - Q1: {Q1_tokens}, Q3: {Q3_tokens}, IQR: {IQR_tokens}")
cleaned_tokens_outliers = df_cleaned[
    (df_cleaned['n_tokens_content'] < (Q1_tokens - 1.5 * IQR_tokens)) |
    (df_cleaned['n_tokens_content'] > (Q3_tokens + 1.5 * IQR_tokens))
]
#Remove outliers from filtered_file.csv
filtered_df_tokens_cleaned = df_cleaned.drop(cleaned_tokens_outliers.index)
filtered_df_tokens_cleaned.to_csv('filtered_tokens_cleaned.csv', index=False)

#Now for shares, stacking on cleaned_tokens_outliers
Q1_shares = filtered_df_tokens_cleaned['shares'].quantile(0.25)
Q3_shares = filtered_df_tokens_cleaned['shares'].quantile(0.75)
IQR_shares = Q3_shares - Q1_shares
print(f"SHARES - Q1: {Q1_shares}, Q3: {Q3_shares}, IQR: {IQR_shares}")
cleaned_shares_outliers = filtered_df_tokens_cleaned[
    (filtered_df_tokens_cleaned['shares'] < (Q1_shares - 1.5 * IQR_shares)) |
    (filtered_df_tokens_cleaned['shares'] > (Q3_shares + 1.5 * IQR_shares))
]
#remove outliers from filtered_tokens_cleaned.csv
final_outliers_removed = filtered_df_tokens_cleaned.drop(cleaned_shares_outliers.index)
final_outliers_removed.to_csv('final_outliers_removed.csv', index=False)


#Self explanatory
weekday_columns = [
    'weekday_is_monday', 'weekday_is_tuesday', 'weekday_is_wednesday',
    'weekday_is_thursday', 'weekday_is_friday', 'weekday_is_saturday',
    'weekday_is_sunday'
]

#Filter for double checked days
filtered_df_weekday = df[df[weekday_columns].sum(axis=1) >= 2]

#Save to file
filtered_df_weekday.to_csv('filtered_days.csv', index=False)


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