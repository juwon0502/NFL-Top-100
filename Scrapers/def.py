from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import json

player_reference_page = "https://www.pro-football-reference.com/players/"


def_weirdos = {
    'Julius Peppers':'P/PeppJu99.htm',
    'Jared Allen':'A/AlleJa22.htm',
    'J. J. Watt':'W/WattJ.00.htm',
    'Mario Williams':'W/WillMa22.htm',
    'Chandler Jones':'J/JoneCh03.htm',
    'Cameron Heyward':'H/HeywCa01.htm',
    'Danielle Hunter':'H/HuntDa01.htm',
    'Frank Clark':'C/ClarFr01.htm',
    'B. J. Raji':'R/RajiBJ99.htm',
    'Chris Jones':'J/JoneCh09.htm',
    'James Harrison':'H/HarrJa23.htm',
    'Patrick Willis':'W/WillPa98.htm',
    'Derrick Johnson':'J/JohnDe25.htm',
    "D'Qwell Jackson":'J/JackDQ20.htm',
    'Aldon Smith':'S/SmitAl04.htm',
    'C. J. Mosley':'M/MoslC.00.htm',
    'Telvin Smith':'S/SmitTe01.htm',
    "Dont'a Hightower":'H/HighDo01.htm',
    'Jaylon Smith':'S/SmitJa05.htm',
    'T. J. Watt':'W/WattT.00.htm',
    'Josh Norman':'N/NormJo01.htm',
    'Marcus Peters':'P/PeteMa00.htm',
    'Chris Harris Jr.':'H/HarrCh01.htm',
    'Janoris Jenkins':'J/JenkJa03.htm',
    'Malcolm Butler':'B/ButlMa01.htm',
    'A. J. Bouye':'B/BouyA.00.htm',
    'Marshon Lattimore':'L/LattMa01.htm',
    "Tre'Davious White":'W/WhitTr01.htm',
    'T. J. Ward':'W/WardT.99.htm',
    'Ha Ha Clinton-Dix':'C/ClinHa00.htm',
    'Kevin Byard':'B/ByarKe01.htm',
    'Eddie Jackson':'J/JackEd01.htm'
}


def_pos = ['DE', 'DT', 'LB', 'CB', 'S']

#make a new df of player's stats from the season
def get_stats(name, year, end):
    if name in def_weirdos:
        end = def_weirdos[name]
    r = requests.get(player_reference_page + end)
    soup = bs(r.content , features = "html.parser")
    try:
        table = soup.find('table').find('tbody').find("tr", attrs = {'id':f'defense.{str(year)}'}).find_all('td')
    except:
        try:
            end2 = end[0:8] + "20.htm"
            r = requests.get(player_reference_page + end2)
            soup = bs(r.content , features = "html.parser")
            table = soup.find('table').find('tbody').find("tr", attrs = {'id':f'defense.{str(year)}'}).find_all('td')
        except:
            try:
                end2 = end[0:8] + "00.htm"
                r = requests.get(player_reference_page + end2)
                soup = bs(r.content , features = "html.parser")
                table = soup.find('table').find('tbody').find("tr", attrs = {'id':f'defense.{str(year)}'}).find_all('td')
            except:
                print(name, year, end2)
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
    r = requests.get('https://www.pro-football-reference.com/players/W/WillMa06.htm')
    soup = bs(r.content , features = "html.parser")
    table = soup.find("table").find_all("th")
    add_cols = [th.text for th in table]
    add_cols = add_cols[15:33]
    add_cols.insert(0,"Player")
    add_cols.insert(1,"Year")
    return add_cols

def main():
    df = pd.read_csv('../Data/Top 100 Players Master Dataset.csv' , index_col = ['Year', 'Player'])
    temp = pd.DataFrame()
    for x in def_pos:
        temp2 = df.loc[df['Position']==x]
        temp = pd.concat([temp,temp2])
    big_list = []
    for name in list(temp.index.values):
        fn = name[1].split(" ")[0]
        ln = name[1].split(" ")[1]
        while len(ln) < 4:
            ln = ln+'x'
        y = name[0]
        tag = ""
        tag = ln[0] + "/" + ln[0:4]
        tag += fn[0:2] + "99.htm"
        row = get_stats(name[1], y, tag)
        big_list.append(row)
        print(name)
    big_list = [x for x in big_list if x]
    def_stats = pd.DataFrame(big_list, columns = get_col_names())
    def_stats = def_stats.set_index(['Year','Player'])
    def_data = temp.join(def_stats, lsuffix=['Year','Player'], rsuffix=['Year','Player'])
    def_data.to_csv('../Data/def_data.csv')
    print(def_data)

main()

