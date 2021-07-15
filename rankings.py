from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
# from matplotlib import pyplot as plt
import json

URLHEAD = "https://en.wikipedia.org/wiki/NFL_Top_100_Players_of_"
YEARS = []
for x in range(2010, 2020):
  YEARS.append(x)

with open('teams.json') as json_file:
    team_abv = json.load(json_file)

with open('position.json') as json_file:
    position_abv = json.load(json_file)

def get_data(year):
  #Get html based on what year
  r = requests.get(URLHEAD + str(year+1))
  soup = bs(r.content , features = "html.parser")
  #find the right table
  tables = soup.find_all('table')
  #from table headers get column names
  headers = tables[2].find('tbody').find_all('th')
  cols = []
  for header in headers:
    cols.append(header.text.strip())
  #Find rest of data
  tr = tables[2].find('tbody').find_all('tr')
  master = []
  row = []
  for ln in tr:
    #fill row with td    
    for td in ln.find_all('td'):
      row.append(td.text.strip())
    master.append(row)
    row = []
  master = master[1:]
  #make first row be column names
  master.insert(0,cols)
  return master

def main():
    #populate dictionary of all individual years and get consistent column names
    df_list = {}
    try:
        del temp_df
    except:
        pass
    for year in YEARS:
        temp_df = pd.DataFrame(get_data(year))
        cols = list(temp_df.iloc[0])
        temp_df = temp_df.iloc[1:]
        temp_df.columns=cols
        try:
            temp_df['Team'] = temp_df[str(year) + ' Team']
        except:
            temp_df['Team'] = temp_df[str(year) + ' team']
        temp_df.drop(temp_df.columns.difference(['Rank', 'Player', 'Position', 'Team', 'Year']), 1, inplace=True)
        temp_df['Year'] = year
        temp_df.head()
        df_list[year] = temp_df

    #concat all indv df into one master df
    df = pd.DataFrame()
    for idx in df_list:
        df = pd.concat([df,df_list[idx]])

    for team in team_abv:
        df.loc[df['Team'].str.contains(team), 'Team'] = team_abv[team]

    for pos in position_abv:
        df.loc[df['Position'].str.match(pos, case = False) , 'Position'] = position_abv[pos]

    df['Rank'] = df['Rank'].astype('int32')
    df['Points'] = 101 - df['Rank']
    df.loc[df['Player'].str.contains('Mark Ingram Jr.')] = 'Mark Ingram'
    df = df.set_index(['Year', 'Player'])
    df.to_csv("Top 100 Players Master Dataset.csv")

main()