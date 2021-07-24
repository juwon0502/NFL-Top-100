from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import json

player_reference_page = "https://www.pro-football-reference.com/players/"


te_weirdos = {
    'Jordan Reed':'R/ReedJo02.htm',
    'Delanie Walker':'W/WalkHu00.htm',
    'Gary Barnidge':'B/BarnGa01.htm',
    'Darren Waller':'W/WallDa01.htm'
}


#make a new df of player's stats from the season
def get_stats(name, year, end):
    if name in te_weirdos:
        end = te_weirdos[name]
    r = requests.get(player_reference_page + end)
    soup = bs(r.content , features = "html.parser")
    try:
        table = soup.find('table').find('tbody').find("tr", attrs = {'id':f'receiving_and_rushing.{str(year)}'}).find_all('td')
    except:
        print(name, year, end)
        return []
    data = [td.text for td in table]
    data = data[6:]
    data1 = []
    for x in data:
        try:
            data1.append(int(x))
        except:
            try:
                data1.append(float(x))
            except:
                data1.append(0)
    data1.insert(0,name)
    data1.insert(1,year)
    return data1

def get_col_names():
    r = requests.get('https://www.pro-football-reference.com/players/H/HillTy00.htm')
    soup = bs(r.content , features = "html.parser")
    table = soup.find("table").find_all("th")
    add_cols = [th.text for th in table]
    add_cols = add_cols[15:40]
    add_cols.insert(0,"Player")
    add_cols.insert(1,"Year")
    return add_cols

def main():
    df = pd.read_csv('../Data/Top 100 Players Master Dataset.csv' , index_col = ['Year', 'Player'])
    te = df.loc[df['Position']=='TE']
    big_list = []
    for name in list(te.index.values):
        fn = name[1].split(" ")[0]
        ln = name[1].split(" ")[1]
        y = name[0]
        tag = ""
        tag = ln[0] + "/" + ln[0:4]
        tag += fn[0:2] + "00.htm"
        row = get_stats(name[1], y, tag)
        big_list.append(row)
        print(name)
    big_list = [x for x in big_list if x]
    te_stats = pd.DataFrame(big_list, columns = get_col_names())
    te_stats = te_stats.set_index(['Year','Player'])
    te_data = te.join(te_stats, lsuffix=['Year','Player'], rsuffix=['Year','Player'])
    te_data.to_csv('../Data/te_data.csv')
    print(te_data)

main()

