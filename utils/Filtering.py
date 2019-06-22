#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 16:48:54 2019

@author: xiaohaoren
"""

import json
import pickle


def Load_All_Info(json_path,pickle_path):
    
    with open(json_path,'r') as fp:
        json_data = json.load(fp)
    with open(pickle_path, 'rb') as fp:
        pickle_data = pickle.load(fp)
    
    keys = list(json_data.keys())
    
    return json_data,pickle_data,keys


def FilteringAndRanking(querys,places,corpus,review_list=None):
    """
    query = ['冷氣','衛生',...]
    place = ['春山茶水舖','小川拉麵',...]
    corpus = {'春山茶水舖':{'不錯':(正向次數,評論編號),'五花肉':(正向分數,評論編號),...}}
    """
    
    scoreboard = {}
    
    for i,place in enumerate(places):
        
        scoreboard[place]=0
        
        if place not in corpus:
            continue
        
        
        for term in querys:
            term_score = 0
            
            if term not in corpus[place]:
                continue
            else:
                keyword_data = corpus[place][term]
                for rid,p in keyword_data.items():
                    term_score += p
                    
                    if review_list is not None:
                        rid = int(rid)
                        review_content = review_list[rid]
                        print('"%s"由於「%s」中的"%s"而加%d分' % (place,review_content,term,p))
                    
            scoreboard[place] += term_score
        
        
        
    return scoreboard
        

if __name__ == "__main__":
    
    corpus_path = '../data/place_dict.json'
    reviewContent_path = '../data/review_list.json'
    querys = ['貴']
    
    coupus,review_list,places = Load_All_Info(json_path=corpus_path,pickle_path=reviewContent_path)
    
    socoreboard = FilteringAndRanking(querys=querys,places=places,corpus=coupus,review_list=review_list)
    
    
    
