from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import json

player_reference_page = "https://www.pro-football-reference.com/players/"

weirdos = {'Robert Griffin III':'G/GrifRo01.htm',
           'Dak Prescott':'P/PresDa01.htm',
           'Josh Allen':'A/AlleJo02.htm',
           'Alex Smith':'S/SmitAl03.htm',
           'Derek Carr':'C/CarrDe02.htm',
           'Marcus Mariota':'M/MariMa01.htm'}

#make a new df of player's stats from the season
def get_stats(name, year, end):
    if name in weirdos:
        end = weirdos[name]
    r = requests.get(player_reference_page + end)
    soup = bs(r.content , features = "html.parser")
    try:
        table = soup.find('table').find('tbody').find("tr", attrs = {'id':f'passing.{str(year)}'}).find_all('td')
    except:
        return []
    data = [td.text for td in table]
    win_loss = data[6]
    win = int(win_loss.split("-")[0])
    loss = int(win_loss.split("-")[1])
    data = data[7:]
    data1 = []
    for x in data:
        try:
            data1.append(int(x))
        except:
            try:
                data1.append(float(x))
            except:
                data1.append(0)
    data1.insert(0,win)
    data1.insert(1,loss)
    data1.insert(0,name)
    data1.insert(1,year)
    return data1

def main():
    df = pd.read_csv("Top 100 Players Master Dataset.csv" , index_col=['Year', 'Player'])
    # populate new df by calling get_stats method
    qb = df.loc[df['Position'] == "QB"]
    big_list = []
    for name in list(qb.index.values):
        fn = name[1].split(" ")[0]
        ln = name[1].split(" ")[1]
        y = name[0]
        tag = ""
        tag = ln[0] + "/" + ln[0:4]
        tag += fn[0:2] + "00.htm"
        row = get_stats(name[1], y, tag)
        print(name)
        big_list.append(row)

    # get rid of empty list in nested list
    big_list = [x for x in big_list if x]
    # create new df with nested list and correct columns. Set year and player as multi-index
    qb_stats = pd.DataFrame(big_list, columns=get_col_names())
    qb_stats = qb_stats.set_index(['Year','Player'])
    qb_data = qb.join(qb_stats, lsuffix=['Year','Player'], rsuffix=['Year','Player'])
    qb_data = qb_data.dropna()
    qb_data.to_csv("qb_data.csv")
    print(qb_data)
    return(qb_data)


def get_col_names():
    # get column names of passing stats
    p = requests.get("https://www.pro-football-reference.com/players/R/RyanMa00.htm")
    soup = bs(p.content , features = "html.parser")
    table = soup.find("table").find_all("th")
    add_cols = [th.text for th in table]
    add_cols = add_cols[8:32]
    add_cols.insert(0,"Wins")
    add_cols.insert(1,"Losses")
    add_cols.insert(0,"Player")
    add_cols.insert(1,"Year")
    return add_cols

main()


