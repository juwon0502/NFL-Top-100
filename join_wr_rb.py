import pandas as pd

wr = pd.read_csv('wr_data.csv' , index_col=['Year','Player'])
rb = pd.read_csv('rb_data.csv' , index_col=['Year','Player'])

rbwr = pd.concat([wr,rb])

rbwr = rbwr.sort_values('YScm' , ascending = False)

df = pd.read_csv('Top 100 Players Master Dataset.csv')
print(len(df.loc[df['Position']=='FB']))