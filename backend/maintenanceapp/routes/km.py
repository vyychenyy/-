#!/usr/bin/python
# coding=utf-8

from flask import Flask,jsonify,make_response,request
from influxdb import InfluxDBClient
import numpy as np
import os
import time,datetime
from array import *
from . import routes
from maintenanceapp import *
from numpy import *
import matplotlib as mpl
import csv
import matplotlib.pyplot as plt

plt.switch_backend('agg') 


# 加载数据
# 加载数据
def loadDataSet():  # 解析文件，按逗号分割字段，得到一个浮点数字类型的矩阵
    dataMat = []              # 文件的最后一个字段是类别标签
    with open('maintenanceapp/static/km.csv') as file:
      reader = csv.DictReader(file)
      test = [test for test in reader]

    key1 = 'bytes_recv'
    key2 = 'bytes_sent'
    i = 1
    while i < len(test):
        temp = []
        num1 = float(test[i]['bytes_sent']) - float(test[i-1]['bytes_sent'])
        num2 = float(test[i]['bytes_recv']) - float(test[i-1]['bytes_recv'])
        temp.append(num1)
        temp.append(num2)
        dataMat.append(temp)
        i += 1
    return dataMat
 
# 计算欧几里得距离
def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2))) # 求两个向量之间的距离
 
# 构建聚簇中心，取k个(此例中为4)随机质心
def randCent(dataSet, k):
    n = shape(dataSet)[1]
    centroids = mat(zeros((k,n)))   # 每个质心有n个坐标值，总共要k个质心
    for j in range(n):
        minJ = min(dataSet[:,j])
        maxJ = max(dataSet[:,j])
        rangeJ = float(maxJ - minJ)
        centroids[:,j] = minJ + rangeJ * random.rand(k, 1)
    return centroids
 
# k-means 聚类算法
def kMeans(dataSet, k, distMeans =distEclud, createCent = randCent):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m,2)))    # 用于存放该样本属于哪类及质心距离
    # clusterAssment第一列存放该数据所属的中心点，第二列是该数据到中心点的距离
    centroids = createCent(dataSet, k)
    clusterChanged = True   # 用来判断聚类是否已经收敛
    while clusterChanged:
        clusterChanged = False;
        for i in range(m):  # 把每一个数据点划分到离它最近的中心点
            minDist = inf; minIndex = -1;
            for j in range(k):
                distJI = distMeans(centroids[j,:], dataSet[i,:])
                if distJI < minDist:
                    minDist = distJI; minIndex = j  # 如果第i个数据点到第j个中心点更近，则将i归属为j
            if clusterAssment[i,0] != minIndex: clusterChanged = True;  # 如果分配发生变化，则需要继续迭代
            clusterAssment[i,:] = minIndex,minDist   # 并将第i个数据点的分配情况存入字典
        #print centroids
        for cent in range(k):   # 重新计算中心点
            ptsInClust = dataSet[nonzero(clusterAssment[:,0].A == cent)[0]]   # 去第一列等于cent的所有列
            if len(ptsInClust)!=0:
                centroids[cent,:] = mean(ptsInClust, axis = 0)  # 算出这些数据的中心点
    return centroids, clusterAssment

# 传入一个点测试是否在落在某个聚类中
def maxDis(centroids,clusterAssment):
    max = zeros(4)
    
    for i in range(len(clusterAssment)):
        tep = int(clusterAssment[i,0])
        if clusterAssment[i,1]>max[tep]:
            max[tep] = clusterAssment[i,1]
    return max

def detect(max,centroids,clusterAssment,x,y): 
   # point = array([x, y])
    flag = 1 #返回1则表示为异常点
    for j in range(len(max)):
        dis = distEclud(centroids[j,:],[x,y])
        if dis < max[j] and max[j] != 0:  #则属于其中一个有效聚类
            flag = 0
            break
    
    return flag
            
    

@routes.route('/km/<float:stamp>')
def test_km(stamp):
    # 用测试数据及测试kmeans算法
    color='rbycgmykw'
    dataMat = mat(loadDataSet()) #读聚类数据

    myCentroids, clustAssing = kMeans(dataMat, 4) #聚类
    max = maxDis(myCentroids,clustAssing) #找到最大半径，传入detect
        # 只需要生成一次聚类
    
    client = InfluxDBClient('localhost',port = 8086,database = 'telegraf');
    #stamp = 1559393670.09

    num1 = int(stamp)
    num2 = num1 - 300
    str1 = 'select "bytes_recv" , "bytes_sent" from net where time >= '+ str(num2) +'s and time <= '+str(num1)+'s and bytes_recv != 0' 
    temp = client.query(str1)
    points = temp.get_points()
    if len(temp) == 0:
        return jsonify({"error code": 416,
      "error message": "Reading data is error"}),416

    ax1 = []
    ax2 = []
    test_recv = []
    test_sent = []
    time = []
    err = []
    bad_domain_x= []
    bad_domain_y = []

    k = 0 
    for items in points:
        ax1.append(items[u'bytes_recv'])
        ax2.append(items[u'bytes_sent'])
        if k != 0 :
            test_recv.append(float(ax1[k])-float(ax1[k-1]))
            test_sent.append(float(ax2[k])-float(ax2[k-1]))
            time.append((items[u'time']))
            
        k += 1

    thelength = len(test_recv)

    

    i = 0
    j = 0
    
    while i < thelength:
        x = test_recv[i]
        y = test_sent[i]
        
        if detect(max,myCentroids,clustAssing,y,x) == 1: 
            err.append(time[i])
            temp =[]
            temp.append(y)
            temp.append(x)
            bad_domain_x.append(y)
            bad_domain_y.append(x)
            j += 1
        i += 1



    
    


    #画图部分注释掉了

    #画圆
    if len(err) != 0:
        plt.plot(bad_domain_x,bad_domain_y,"ro",color='#000000')
    for i in range(len(dataMat)):
        plt.plot(dataMat[i,0],dataMat[i,1],"ro",color=color[int(clustAssing[i,0])])
    for i in range(len(myCentroids)):
        plt.plot(myCentroids[i,0],myCentroids[i,1],"ro",color='#9370DB')
        a = myCentroids[i,0]
        b = myCentroids[i,1]
        r = max[i]
        theta = arange(0,2*pi,0.01)
        x = a + r * cos(theta)
        y = b + r * sin(theta) 
        plt.plot(x, y)
    
    '''
    #画四个图
    plt.subplot(2,2,1)#第一张：dataMat
    for i in range(len(dataMat)):
        plt.plot(dataMat[i,0],dataMat[i,1],"ro")

    plt.subplot(2,2,2)#第二张:myCentroids
    for i in range(len(myCentroids)):
        plt.plot(myCentroids[i,0],myCentroids[i,1],"ro",color=color[i])
     
    plt.subplot(2,2,3)#第三张：聚类结果图
    for i in range(len(clustAssing)):
        plt.plot(clustAssing[i,0],clustAssing[i,1],"ro",color=color[int(clustAssing[i,0])])
     
    plt.subplot(2,2,4)#第四张：dataMat聚类结果染色图
    for i in range(len(dataMat)):
        plt.plot(dataMat[i,0],dataMat[i,1],"ro",color=color[int(clustAssing[i,0])])
    for i in range(len(myCentroids)):
        plt.plot(myCentroids[i,0],myCentroids[i,1],"ro",color='#000000')
    '''

    filename = 'kMeans'+ str(stamp)+".png"
   
 

  
    plt.savefig('maintenanceapp/static/'+filename)
    os.system("cd maintenanceapp/static && python test.py")
    

    if len(err) == 0:
        return jsonify({'count':0,
          'time':err,
          'filename':filename})
    else:
        return jsonify({'count':j,
            'time':err,
            'filename': filename})
        
