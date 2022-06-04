from requests_html import HTMLSession
import requests
import json
import threading

output = []
round = 0
total_rounds = 1
num_threads = 1

lock = threading.Lock()
opensea_address = "https://api.opensea.io/api/v1/bundles?limit=50&offset="

with open('data.json') as f:
    output = json.load(f)


def collect_data(thread_number):
    input = []
    data = []
    names = []
    offest = thread_number * 200 * 50
    page = 0
    

    collections = dict()
    with open('val.json') as f:
        input = json.load(f)
    for row in input:
        collections[row['Name']] = row

    while True:
        # print('Collecting Data on Page: ' + str(page), end='\r')
        try:
            response = requests.get(opensea_address + str(offest))
        except:
            print(response)
            break
        response_dict = json.loads(response.text)
        try:
            for collection in response_dict['bundles']: 
                name = ''
                try:
                    name = collection['asset_contract']['name']
                except:
                    continue
                print(name)
                if name in collections: 
                    d = dict()
                    d['name'] = name
                    d['chain'] = collections[name]['Chain']
                    d['volume'] = collections[name]['Volume']
                    d['mkt_cap'] = collections[name]['Market_Cap']
                    d['floor'] = collections[name]['Floor_Price']
                    d['avg_price'] = collections[name]['Avg_Price']
                    d['sales'] = collections[name]['Sales']
                    d['assets'] = collections[name]['Assets']
                    d['owners'] = collections[name]['Owners']
                    d['percent_owners'] = collections[name]['Percent_Owners']
                    # d['slug'] = collection['slug']
                    d['address'] = collection['asset_contract']['address']
                    d['royalties'] = collection['asset_contract']['dev_seller_fee_basis_points']
                    if d not in data:
                        data.append(d)
                        names.append(name)
            offest += 50
            page += 1
        except KeyError:
            # print(page)
            break
    #need to block other threads
    with lock:
        output.extend(data)
        # print('Data Collection Complete on Thread ' + str(thread_number / 50))
        # print(names)

def save_json(filename, data):
    print('Saving Data to ' + filename)
    with open(filename, 'w') as f: 
        json.dump(data, f)


# while round <= total_rounds:
#     print("Creating Threads for Round: " + str(round) + ' of ' + str(total_rounds), end='\r')
#     threads = [] 
#     for i in range(0, num_threads):
#         threads.append(threading.Thread(target=collect_data, args=(i + round * 8,)))
#     # print('Threads Created, Beginning Round: ' + str(round))
#     for thread in threads:
#         thread.start()

#     for thread in threads:
#         thread.join()
#     # print('Threads Joined on Round: ' + str(round))
#     round += 1
collect_data(0)
print()
print('Cleaning Data: Removing Duplicates:')
save_json('data4.json', list({v['name']:v for v in output}.values()))



#{"Name": "Elftown.wtf", "Chain": "Ethereum", "Volume": 1161.54, "Market_Cap": 1225.17, 
# "Floor_Price": 0.159, "Avg_Price": 0.1895, "Sales": 6129, "Assets": 9987, "Owners": 4656, 
# "Percent_Owners": 46.62}

