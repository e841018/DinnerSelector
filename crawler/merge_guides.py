import json
import os
from os import listdir


data_path = 'local_guides'

place_list = listdir(data_path)
guides_list = {} #id:num
threshold = 5
for place in place_list:
    
    f = open(os.path.join(data_path, place))
    json_data = json.load(f)
    
    for guides in json_data:
        ID = guides['ID']
        if ID not in guides_list:
            guides_list[ID] = 1
        else:
            guides_list[ID] += 1
        
guides_list = sorted(guides_list.items(), key=lambda d: d[1], reverse = True)
        
f = open('guides.txt', 'w')
    

for i in guides_list:
    if i[1] > threshold:
        f.write(i[0]+'\n')
        

f.close()
