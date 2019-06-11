import numpy as np
import json
import os
from os import listdir

data_path = '../data/reviews_guide'
guides_list = []
place_list = []

f_guides = open('guides.txt')
f_place = open('places.txt')

guides_file_list = listdir(data_path)

for i in f_guides:
    guides_list.append(i)
    
for i in f_place:
    i = i.split(',')
    place_list.append(i)

normalize_array = np.zeros((len(place_list), len(guides_list)))

for g_idx, guides in enumerate(guides_list):
    for file_name in guides_file_list:
        if(file_name.find(guides[:-1]) != -1):
            guides_path = os.path.join(data_path, file_name)
            break
    
    f_guides = open(guides_path)
    json_data = json.load(f_guides)
    
    guides_place_list = {}
    
    for place in json_data:
        name = place['place']
        address = place['address']
        start = place['stars']
        guides_place_list[(name, address)] = start
        
    for p_idx, place in enumerate(place_list):
        if (place[0], place[1][:-1]) in guides_place_list:
            normalize_array[p_idx][g_idx] = guides_place_list[(place[0], place[1][:-1])]
        else:
            normalize_array[p_idx][g_idx] = 0
            
mean = np.mean(normalize_array, axis = 0)
normalize_array = normalize_array - mean

f = open('normalize_array.txt', 'w')

for i in normalize_array:
    for j in i:
        f.write(str(j) + ',')
    f.write('\n')