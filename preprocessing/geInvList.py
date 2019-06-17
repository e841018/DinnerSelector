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

cg = CorpusGenerator()

files = [join(review_path, f) for f in listdir(review_path) if isfile(join(review_path, f))]

for file in files:
    
    reviews,places = cg.get_review_content(file)
    
    for review,place in zip(reviews,places):
        
        # init place in places_dict
        if place not in places_dict:
            places_dict[place] = dict()
        
        for term in review:
            
            # init term in inv_list
            if term not in inv_list:
                inv_list[term] = list()
            
            # processing places_dict
            if term not in places_dict[place]:
                places_dict[place][term]=0
            places_dict[place][term]+=1
            
            # processing inv_list
            inv_list[term].append(place)
            
            
for term in inv_list.keys():
    inv_list[term] = dict(Counter(inv_list[term]))
            
            
            
            
            
            