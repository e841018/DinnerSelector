#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 00:41:04 2019

@author: xiaohaoren
"""


import jieba.posseg as pseg
import json
import tensorflow as tf
import tensorflow.keras as keras
import numpy as np

from tensorflow.keras import layers



class NLPModule(keras.Model):
    
    def __init__(self
                 ,max_seq_len   = 30
                 ,num_vocab     = 1000
                 ,embedding_dim = 8
                 ,lstm_unit     = 128
                 ,dense_unit    = 256
                 ,num_class     = 1):
        
        super(NLPModule, self).__init__(name='nlp')
        
        
        # Init parameters
        self.max_seq_len = max_seq_len
        self.num_vocab = num_vocab
        self.embedding_dim = embedding_dim
        self.lstm_unit = lstm_unit
        self.dense_unit = dense_unit
        self.num_class = num_class
        
        # Initial Tokenizer
        self.tokenizer = keras.preprocessing.text.Tokenizer(num_words=num_vocab)
        
        # Establish NLP LSTM Network
        self.embedding_layer = layers.Embedding(num_vocab,embedding_dim,input_length=self.max_seq_len)
        self.lstm_layer = layers.LSTM(lstm_unit)
        self.dense1 = layers.Dense(dense_unit,activation="relu")
        self.dense2 = layers.Dense(num_class,activation="linear")
        
    
    def texts_to_sequences(self,corpus):
        
        # Tokenizer :  Word  -> Word Index  + Zero Padding
        
        self.tokenizer.fit_on_texts(corpus)
    
        sequences = self.tokenizer.texts_to_sequences(corpus)
        
        sequences = keras.preprocessing.sequence.pad_sequences(sequences,maxlen=self.max_seq_len)
        
        return sequences
        
    def call(self,inputs,training = False):
        
        x = self.embedding_layer(inputs)
        
        x = self.lstm_layer(x)
        
        x = self.dense1(x)
        
        x = self.dense2(x)
        
        return x



# Word Segmentation ( loading data )
def get_text_from_json(path = '../data/example_guide.json'):
    
    texts = []
    
    with open(path,'r') as f:
        pkg = json.load(f)
    
    
    for review in pkg:
        
        text = review['content']
        
        pairs = [pair for pair in pseg.cut(text)]
        
        # remove stop word
        words = [word for word,flag in pairs if flag != 'x'] 
        
        if len(words) > 0:
            texts.append(words)
    
    return texts



if __name__ == '__main__':
    
    texts = get_text_from_json(path = '../data/example_guide.json')
    
    model = NLPModule()
    
    model.compile(optimizer='adam',loss = tf.losses.MeanSquaredError())
    
    x_train = model.texts_to_sequences(texts)
    
    y_train = np.random.rand(x_train.shape[0])
    
    
    

    
    