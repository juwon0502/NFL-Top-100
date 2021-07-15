from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import json

player_reference_page = "https://www.pro-football-reference.com/players/"

fb_weirdos = {
}

#make a new df of player's stats from the season
def get_stats(name, year, end):
    if name in fb_weirdos:
        end = fb_weirdos[name]
    r = requests.get(player_reference_page + end)
    soup = bs(r.content , features = "html.parser")
    try:
        table = soup.find('table').find('tbody').find("tr", attrs = {'id':f'rushing_and_receiving.{str(year)}'}).find_all('td')
    except:
        table = soup.find('table').find('tbody').find("tr", attrs = {'id':f'receiving_and_rushing.{str(year)}'}).find_all('td')
        print(name, year, end)
        # return []
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
    r = requests.get('https://www.pro-football-reference.com/players/K/KamaAl00.htm')
    soup = bs(r.content , features = "html.parser")
    table = soup.find("table").find_all("th")
    add_cols = [th.text for th in table]
    add_cols = add_cols[15:40]
    add_cols.insert(0,"Player")
    add_cols.insert(1,"Year")
    return add_cols

def main():
    df = pd.read_csv('Top 100 Players Master Dataset.csv' , index_col = ['Year', 'Player'])
    fb = df.loc[df['Position']=='FB']
    big_list = []
    for name in list(fb.index.values):
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
    fb_stats = pd.DataFrame(big_list, columns = get_col_names())
    fb_stats = fb_stats.set_index(['Year','Player'])
    fb_data = fb.join(fb_stats, lsuffix=['Year','Player'], rsuffix=['Year','Player'])
    fb_data.to_csv('fb_data.csv')
    print(fb_data)

main()

