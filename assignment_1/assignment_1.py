import pandas as pd

df = pd.read_csv('OnlineNewsPopularity.csv')
df.info()

#print(df.isnull().sum()) #ingen null verdier
#print(df.duplicated().sum()) #ingen duplikater
#print(df.to_string()) #printer ut alt be careful
