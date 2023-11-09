from bs4 import BeautifulSoup
import json

entries = []
with open("data-no-empties-with-html.json.partial") as f:
    for i in f.readlines():
        entry = json.loads(i)
        if description := BeautifulSoup(entry['link_html']).find('div', attrs = {'id': 'primary'}).text:
           entry['desc'] = description
        print(json.dumps(entry))
