import json

royalties = []
collections = []


with open('test.json') as f:
    royalties = json.load(f)
print(len(royalties))
for i in range(1, 4):
    with open('test' + str(i) + '.json') as f:
        royalties.extend(json.load(f))
    print(len(royalties))

l= list({v['name']:v for v in royalties}.values())

print(len(l))

with open('val.json') as f:
    collections = json.load(f)

def save_json(filename, data):
    print('Saving Data to ' + filename)
    with open(filename, 'w') as f: 
        json.dump(data, f)
i = 0
for collection in collections: 
    if collection['Name'] in royalties: 
       print(i, end='/r')
       i += 1 

save_json('output.json', royalties)
