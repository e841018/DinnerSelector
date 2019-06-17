#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 16:14:53 2019

@author: xiaohaoren
"""

import sys
sys.path.append("../utils")

from w2v import CorpusGenerator
from collections import Counter
from os import listdir
from os.path import isfile, join



places_dict = dict()
inv_list = dict()

review_path = '../data/reviews_guide/'

negative_words = ['不涼','沒','沒有','不','不太','很不']


cg = CorpusGenerator()

files = [join(review_path, f) for f in listdir(review_path) if isfile(join(review_path, f))]

for file in files:
    
    reviews,places = cg.get_review_content(file)
    
    for review,place in zip(reviews,places):
        
        # init place in places_dict
        if place not in places_dict:
            places_dict[place] = dict()
        
        for i,term in enumerate(review):
            
            # init term in inv_list
            if term not in inv_list:
                inv_list[term] = list()
            
            # 此字是否為負面詞意?
            if term in negative_words:
                
                pre_term = 'XX'
                post_term = 'XX'
                
                # 扣分
                if i>0:
                    # 前字
                    pre_term = review[i-1]
                    places_dict[place][pre_term]-=2
                    
                if i<len(review)-1:
                    # 後字
                    post_term = review[i+1]
                    if post_term not in places_dict[place]:
                        places_dict[place][post_term]=0
                    places_dict[place][post_term]-=2
                    
                print(pre_term+term+post_term)
            
            # processing places_dict
            if term not in places_dict[place]:
                places_dict[place][term]=0
            places_dict[place][term]+=1
            
            # processing inv_list
            inv_list[term].append(place)
            
            
for term in inv_list.keys():
    inv_list[term] = dict(Counter(inv_list[term]))
            
            
            
            
            
            