from requests_html import HTMLSession
import json 

root_address = 'https://coinmarketcap.com/nft/collections/'

session = HTMLSession()
data = []


def collect_data(pages):
    for page in pages: 
        #https://coinmarketcap.com/nft/collections/?page=2
        r = session.get(root_address + '?page=' + str(page))
        r.html.render(scrolldown=16, sleep=0.1, timeout=30.0)
        rows = r.html.find('tbody tr')
        for row in rows:
            d = dict() 
            columns = row.find('td')
            d['Name'] = columns[1].text.split("\n", 1)[0]
            
            try: 
                d['Chain'] = columns[1].text.split("\n", 1)[1]
                if d['Chain'] != 'Ethereum':
                    continue
            except IndexError:
                d['Chain'] = 'n/a'
            
            try:
                d['Volume'] = float(columns[2].text.split(" ", 1)[0].replace(',', ''))
            except ValueError:
                d['Volume'] = 'n/a'
            
            try:
                d['Market_Cap'] = float(columns[3].text.split(" ", 1)[0].replace(',', ''))
            except ValueError:
                d['Market_Cap'] = 'n/a'

            try:
                d['Floor_Price'] = float(columns[4].text.split(" ", 1)[0])
            except ValueError:
                d['Floor_Price'] = 'n/a'
            try:
                d['Avg_Price'] = float(columns[5].text.split(" ", 1)[0].replace(',', ''))
            except:
                d['Avg_Price'] = 'n/a'
            d['Sales'] = int(columns[6].text.split("\n", 1)[0].replace(',', ''))
            
            try:
                d['Assets'] = int(columns[7].text.replace(',', ''))
            except ValueError:
                d['Assets'] = 'n/a'
            
            d['Owners'] = int(columns[8].text.replace(',', ''))

            try:
                d['Percent_Owners'] = float(columns[9].text.split(" ", 1)[0])
            except ValueError:
                d['Percent_Owners'] = 'n/a'
            # print(d)
            data.append(d)

def save_json(data):
    with open('val.json', 'w') as f: 
        json.dump(data, f)

pages = list(range(1, 25))
collect_data(pages)
save_json(data)
print(data)

