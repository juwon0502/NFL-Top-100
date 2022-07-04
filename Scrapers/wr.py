from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import json

player_reference_page = "https://www.pro-football-reference.com/players/"


wr_weirdos = {
    'Andre Johnson':'/J/JohnAn02.htm',
    'Mike Williams':'W/WillMi04.htm',
    'Steve Smith':'S/SmitSt01.htm',
    'A. J. Green':'G/GreeA.00.htm',
    'Hakeem Nicks':'N/NickHa01.htm',
    'Julio Jones':'J/JoneJu02.htm',
    'Dez Bryant':'B/BryaDe01.htm',
    'Demaryius Thomas':'T/ThomDe03.htm',
    'Josh Gordon':'G/GordJo02.htm',
    'Antonio Brown':'B/BrowAn04.htm',
    'Pierre Garçon':'G/GarcPi00.htm',
    'Allen Robinson':'R/RobiAl02.htm',
    'Allen Hurns':'H/HurnAl01.htm',
    'Michael Thomas':'T/ThomMi05.htm',
    'Davante Adams':'A/AdamDa01.htm',
    'Robert Woods':'W/WoodRo02.htm',
    'Corey Davis':'D/DaviCo03.htm'
}


#make a new df of player's stats from the season
def get_stats(name, year, end):
    if name in wr_weirdos:
        end = wr_weirdos[name]
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
    data1 = data1[0:27]
    return data1

def get_col_names():
    r = requests.get('https://www.pro-football-reference.com/players/H/HillTy00.htm')
    soup = bs(r.content , features = "html.parser")
    table = soup.find("table").find_all("th")
    add_cols = [th.text for th in table]
    add_cols = add_cols[16:41]
    add_cols.insert(0,"Player")
    add_cols.insert(1,"Year")
    return add_cols

def main():
    df = pd.read_csv('../Data/Top 100 Players Master Dataset.csv' , index_col = ['Year', 'Player'])
    wr = df.loc[df['Position']=='WR']
    big_list = []
    for name in list(wr.index.values):
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
    wr_stats = pd.DataFrame(big_list, columns = get_col_names())
    wr_stats = wr_stats.set_index(['Year','Player'])
    wr_data = wr.join(wr_stats, lsuffix=['Year','Player'], rsuffix=['Year','Player'])
    wr_data.to_csv('../Data/wr_data.csv')
    print(wr_data)

main()

