#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 16:14:53 2019

@author: xiaohaoren
"""
import re
import json
import pickle
import sys
sys.path.append("../utils")

from w2v import CorpusGenerator
from os import listdir
from os.path import isfile, join



places_dict = dict()
review_list = []
negative_words = ['不涼','沒','沒有','不','不足','不佳','不太','不行','很不','很差','不好']
review_path = '../data/reviews_place/'

save_path_corpus = '../data/place_dict.json'
save_path_list = '../data/review_list.json'
cg = CorpusGenerator()


files = [join(review_path, f) for f in listdir(review_path) if isfile(join(review_path, f))]

for file in files:
    
    reviews,reviews_origin = cg.get_placeReview_content(file)
    a,b = re.search('place=.* coord', file).span()
    place = file[a+6:b-6]        
    
    places_dict[place] = dict()
    
    # for each reivew in reviews of the restaurant
    for review,review_origin in zip(reviews,reviews_origin):
        
        review_list.append(review_origin)
        review_id = len(review_list)-1
        
        for i,term in enumerate(review):
            
            # processing places_dict
            if term not in places_dict[place]:
                places_dict[place][term]={}
            if review_id not in places_dict[place][term]:
                places_dict[place][term][review_id]=0
            places_dict[place][term][review_id]+=1
            
            
            # 此字是否為負面詞意?
            if term in negative_words:
                
                pre_term = 'XX'
                post_term = 'XX'
                
                # 扣分
                if i>0:
                    # 前一字
                    pre_term = review[i-1]
                    places_dict[place][pre_term][review_id]-=2
                    
                if i<len(review)-1:
                    # 後一字
                    post_term = review[i+1]
                    if post_term not in places_dict[place]:
                        places_dict[place][post_term]={}
                    if review_id not in places_dict[place][post_term]:
                        places_dict[place][post_term][review_id]=0
                    places_dict[place][post_term][review_id]-=2
                    
                print(pre_term+term+post_term,'by',review_id)
            
            
with open(save_path_corpus, 'w') as fp:
    json.dump(places_dict, fp)       
            
with open(save_path_list, 'wb') as fp:
    pickle.dump(review_list, fp)