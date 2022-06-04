import requests
import json

# offest = 0
# url = "https://api.opensea.io/api/v1/bundles?limit=50&offset="

# response = requests.get(url + str(offest))

# print(response.status_code)
# o = json.loads(response.text)

# # print(json.dumps(o['bundles'][0], sort_keys=False, indent=4))
# print(len(o['bundles']))


url = "https://api.opensea.io/api/v1/collections?offset=" + str(100) + "&limit=300"

headers = {"Accept": "application/json"}

response = requests.get(url, headers=headers)

print(response)
o = json.loads(response.text)
print(json.dumps(o['collections'][0], sort_keys=False, indent=4))
print(o['collections'][0]['slug'])
print(o['collections'][0]['dev_seller_fee_basis_points'])
print(o['collections'][0]['dev_seller_fee_basis_points'])


# from requests_html import HTMLSession
# import json 

# data = []
# root_address = 'https://nftvaluations.com/'
# session = HTMLSession()

# with open('val.json') as f:
#    data = json.load(f)

# def collect_data():
#     r = session.get(root_address)
#     r.html.render(scrolldown=16, sleep=0.1, timeout=30.0)
#     print(1)


# print(data)
# print(len(data))