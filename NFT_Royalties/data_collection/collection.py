from requests_html import HTMLSession
import requests
import json
import threading

output = []
round = 0
total_rounds = 1
num_threads = 1
lock = threading.Lock()
opensea_address = "https://api.opensea.io/api/v1/collections?offset="
headers = {"Accept": "application/json"}
largest_offset = 0

# with open('data.json') as f:
#     output = json.load(f)


def collect_data(thread_number):
    input = []
    data = []
    names = []
    offset = thread_number * 200 
    collections = dict()

    with open('val.json') as f:
        input = json.load(f)
    for row in input:
        collections[row['Name']] = row

    while offset <= 50300:
        try:
            response = requests.get(opensea_address + str(offset) + "&limit=300", headers=headers)
        except response.status_code != 200:
            print(response)
            break
        response_dict = json.loads(response.text)
        try:
            for collection in response_dict['collections']: 
                if len(collection['primary_asset_contracts']) > 0:
                    name = collection['primary_asset_contracts'][0]['name']
                    d = dict()
                    d['name'] = name
                    d['slug'] = collection['slug']
                    d['address'] = collection['primary_asset_contracts'][0]['address']
                    d['royalties'] = collection['primary_asset_contracts'][0]['dev_seller_fee_basis_points']
                    if d not in data:
                        data.append(d)
                        names.append(name)
            offset += 300
            print("Offset: " + str(offset), end='\r')
        except KeyError:
            break
    #need to block other threads
    output.extend(data)


def save_json(filename, data):
    print('Saving Data to ' + filename)
    with open(filename, 'w') as f: 
        json.dump(data, f)


# while round <= total_rounds:
#     print("Creating Threads for Round: " + str(round) + ' of ' + str(total_rounds), end='\r')
#     threads = [] 
#     for i in range(0, num_threads):
#         threads.append(threading.Thread(target=collect_data, args=(i + round * 8,)))
#     for thread in threads:
#         thread.start()

#     for thread in threads:
#         thread.join()
#     round += 1

collect_data(0)
print()
# print(output)
print('Cleaning Data: Removing Duplicates:')
save_json('test3.json', list({v['name']:v for v in output}.values()))



#{"Name": "Elftown.wtf", "Chain": "Ethereum", "Volume": 1161.54, "Market_Cap": 1225.17, 
# "Floor_Price": 0.159, "Avg_Price": 0.1895, "Sales": 6129, "Assets": 9987, "Owners": 4656, 
# "Percent_Owners": 46.62}

