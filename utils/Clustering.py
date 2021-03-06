#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 19:13:22 2019

@author: xiaohaoren
"""

import tensorflow as tf
import matplotlib
from matplotlib import pyplot as plt

print(tf.__version__)

def distance_L2(data,centers):
    # check dimension equal
    assert centers.shape[1] == data.shape[1]
    # data:(n,dim) broadcast to (n,k,dim)
    data_bc = tf.broadcast_to(tf.expand_dims(data,1),[data.shape[0],centers.shape[0],centers.shape[1]])
    # centers:(k,dim) expand to (1,k,dim)
    centers_exp = tf.expand_dims(centers, [0])
    # vector operation (1,k,dim)-(n,k,dim)
    diff = (centers_exp - data_bc)**2
    # result:(n,k,dim)->(n,k)
    return tf.reduce_sum(diff,axis=2)

def distance_Cos(data,centers):
    # check dimension equal
    assert centers.shape[1] == data.shape[1]
    # data:(n,dim) broadcast to (n,k,dim)
    data_bc = tf.broadcast_to(tf.expand_dims(data,1),[data.shape[0],centers.shape[0],centers.shape[1]])
    # centers:(k,dim) expand to (1,k,dim)
    centers_exp = tf.expand_dims(centers, [0])
    
    # norm : (n,k)
    data_norm = tf.sqrt(tf.reduce_sum(tf.square(data_bc), axis=2))
    centers_norm = tf.sqrt(tf.reduce_sum(tf.square(centers_exp), axis=2))
    # inner product : (n,k)
    inner_product = tf.reduce_sum(tf.multiply(data_bc,centers_exp),axis=2)
    # Cosine : (n,k)
    cos = inner_product/(data_norm*centers_norm)
    return cos
    
def predict(data,centers,distance=distance_L2):
    
    if distance==distance_L2:
        method = tf.argmin
    else:
        method = tf.argmax
    distances = distance(data,centers)
    
    # find out k with the smallest distance
    return method(distances,axis=1)

def update(datas,predicts):
    indices = tf.argsort(predicts)
    sort_datas = tf.gather(datas, indices)
    sort_predicts = tf.gather(predicts, indices)
    return tf.math.segment_mean(sort_datas, sort_predicts)
    
def evaluate(datas,predicts,centers,distance=distance_L2):
    k_dist = tf.reduce_min(distance(datas,centers),axis=1)
    return tf.reduce_mean(k_dist).numpy()

def Kmeans(datas,k,epoch=10,distance=distance_L2):
    
    N,dim = datas.shape
    center_idx = tf.random.uniform([k],minval=0,maxval=N-1,dtype=tf.int32)
    centers = tf.gather(datas,center_idx)
    
    for i in range(epoch):
        predicts = predict(datas,centers,distance=distance)
        centers = update(datas,predicts)
        loss = evaluate(datas,predicts,centers)
        print('round %d , avg. distance = %f' % (i+1,loss))
        
        if dim == 2 :
            x,y = tf.split(datas,2,1)
            x = tf.squeeze(x)
            y = tf.squeeze(y)
            colors = ['red','green','blue','yellow','purple','pink', "orange","gold", "limegreen"]
            fig = plt.figure()
            plt.scatter(x, y, c=predicts, cmap=matplotlib.colors.ListedColormap(colors))
            cx,cy = tf.split(centers,2,1)
            cx = tf.squeeze(cx)
            cy = tf.squeeze(cy)
            plt.plot(cx,cy,'k+',markersize=12)
            plt.title('avg dist = '+str(loss))
            plt.show()

    return predicts

def KNN(target,datas,k,clusters=None,distance=distance_L2):
    if len(target.shape) < 2:
        target = tf.expand_dims(target,0)
    
    dim = target.shape[-1]
    distances = tf.squeeze(distance(target,datas))
    if distance==distance_L2:
        k_nearest = tf.argsort(distances)[0:k]
    else:
        k_nearest = tf.argsort(distances)[-k-1:-1]
        
    if clusters != None:
        predicts = tf.gather(clusters,k_nearest)
    else:
        predicts = tf.convert_to_tensor([-1]*k)
    
    if dim == 2 :
        x,y = tf.split(datas,2,1)
        x = tf.squeeze(x)
        y = tf.squeeze(y)
        colors = ['red','green','blue','yellow','purple','pink', "orange","gold", "limegreen"]
        fig = plt.figure()
        plt.scatter(x, y, c=clusters, cmap=matplotlib.colors.ListedColormap(colors))
                   
        nd = tf.gather(datas,k_nearest)
        nx = tf.gather(nd,0,axis=1)
        ny = tf.gather(nd,1,axis=1)
        plt.plot(nx,ny,'k4',markersize=14)
        
        tx = tf.gather(target,0,axis=1)
        ty = tf.gather(target,1,axis=1)
        plt.plot(tx,ty,'k*',markersize=12)
        plt.title(str(predicts.numpy()))
    
    return predicts,k_nearest


if __name__ == '__main__':
    data1 = tf.random.uniform([30,2],minval=0,maxval=25)
    data2 = tf.random.uniform([30,2],minval=10,maxval=35)
    data3 = tf.random.uniform([30,2],minval=30,maxval=45)
    
    datas = tf.concat([data1,data2,data3],axis=0)
    tf.random.shuffle(datas,seed=1024)


    # Setting the distance rule
    distance = distance_L2

    # Test Kmeans
    clusters = Kmeans(datas=datas,k=6,epoch=5,distance=distance)
    
    # Test KNN
    target = tf.random.uniform([1,2],minval=0,maxval=50)
    prediction = KNN(target,datas,5,clusters=clusters,distance=distance)


