#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 16:48:54 2019

@author: xiaohaoren
"""





def Filtering(querys,places,corpus,review_list):
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
                    
                    #print('"%s"因為%d中的%s而加%d分' % (place,rid,term,p))
                    print('"%s"因為「%s」中的"%s"而加%d分' % (place,review_list[rid],term,p))
                    
            scoreboard[place] += term_score
        
        
        
    return scoreboard
        