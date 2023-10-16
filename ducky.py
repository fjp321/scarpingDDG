import pandas as pd
import plotly.express as px
import requests
import datetime
import time
from bs4 import BeautifulSoup

queries = [
    'dwm',
    'hyprland',
    'gnome',
    'kde',
    'qtile',
    'awesome',
    'cinnamon',
    'bspwm',
    'i3',
    'sway',
    'mutter'
]
windows = {'day':(datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
    'week':(datetime.datetime.now()-datetime.timedelta(days=7)).strftime("%Y-%m-%d"),
    'month':(datetime.datetime.now()-datetime.timedelta(days=20)).strftime("%Y-%m-%d"),
#    '3_months':(datetime.datetime.now()-datetime.timedelta(days=90)).strftime("%Y-%m-%d"),
    '6_months':(datetime.datetime.now()-datetime.timedelta(days=180)).strftime("%Y-%m-%d"),
#    'year':(datetime.datetime.now()-datetime.timedelta(days=365)).strftime("%Y-%m-%d")
}
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:119.0) Gecko/20100101 Firefox/117.0'
}
d = {'wm': [], 'window': [], 'count':[]}
df = pd.DataFrame(data=d)
for window in windows:
    for query in queries:
        term = 'intitle%3A{}+site%3Areddit.com/r/unixporn+after%3A{}'.format(query,windows[window])
        address = 'http://www.google.com/search?q='
        newword = address + term
        time.sleep(5)
        page = requests.get(newword, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        phrase_extract = soup.find(id="result-stats")
        try:
          count = int(phrase_extract.text.split(' ')[1].replace(',',''))
        except:
          count = int(phrase_extract.text.split(' ')[0].replace(',',''))
        df.loc[-1] = [query, window, count]
        df.index = df.index + 1
        df = df.sort_index()
print(df)

fig = px.bar(df.sort_values(by='count', ascending=False), x="wm", y="count", color="window", title="Historic Unixporn Window Managers Posts", barmode='overlay')
fig.show()

