import json
import os
from os import listdir

data_path = '../data/reviews_guide'

guides_list = listdir(data_path)
place_list = {} 
valid_list = []
threshold = 10 #6
for guide in guides_list:
    
    f = open(os.path.join(data_path, guide), encoding='utf-8')
    json_data = json.load(f)
    
    for place in json_data:
        name = place['place']
        address = place['address']
        if (name, address) not in place_list:
            place_list[(name, address)] = 1
        else:
            place_list[(name, address)] += 1
            
place_list = sorted(place_list.items(), key=lambda d: d[1], reverse = True)

for place in place_list:
    judge = 'f'
    if place[1] > threshold:
        # judge = input(place[0])
    # if judge == '\'':
        valid_list.append(place[0])

with open('places.json', 'w', encoding='utf-8') as f:
    json.dump(valid_list, f, ensure_ascii=False)