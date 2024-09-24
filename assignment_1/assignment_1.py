import pandas as pd

df = pd.read_csv('OnlineNewsPopularity.csv')
df.info()

print(df.to_string())
