import pandas as pd
from get_df import get_information_df

df = get_information_df()

print(df.head())
print(df.columns.tolist())

