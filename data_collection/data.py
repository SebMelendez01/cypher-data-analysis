import json

input = []
output = []

with open('data2.json') as f:
        input = json.load(f)

with open('data2.json') as f:
        input.extend(json.load(f))

output = list({v['name']:v for v in input}.values())
print(len(output))






