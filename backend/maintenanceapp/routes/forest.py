import csv
from sklearn.ensemble import IsolationForest
from flask import Flask,jsonify,make_response,request
from influxdb import InfluxDBClient
import numpy as np
import os
import time,datetime
from array import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
plt.switch_backend('agg')  
from . import routes
from maintenanceapp import *
import os
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

@routes.route('/forest/<float:stamp>')
def test_ioforest(stamp):

  '''
  with open('maintenanceapp/static/net.csv','rb') as file:
      reader = csv.DictReader(file)
      test = [test for test in reader]
  '''
  '''

  with open('test1.csv','rb') as file1:
      reader1 = csv.DictReader(file1)
      test1 = [item for item in reader1]
  '''

  client = InfluxDBClient('localhost',port = 8086,database = 'telegraf');
  #stamp = time.time()  
  num1 = int(stamp)
  num2 = num1 - 300
  str1 = 'select "bytes_recv" , "bytes_sent" from net where time >= '+ str(num2) +'s and time <= '+str(num1)+'s and bytes_recv != 0' 
  temp = client.query(str1)
  test1 = temp.get_points()
  
  if len(temp) == 0:
    return jsonify({"error code": 416,
      "error message": "Reading data is error"}),416

 # thelength = len(test)
  apache = []
  apache2 = []
  origin = []
  apache1 = []
  apache21 = []
  origin1 = []
  time_store = []
  key = 'bytes_recv'
  key2 ='bytes_sent'
  key3 = 'time'
  i = 0
  '''
  while i < thelength:
      apache.append(test[i][key])
      apache2.append(test[i][key2])
      time_store.append(test[i][key3])

      if i!=0:
        train_req = float(apache[i])- float(apache[i-1])
        train_sec = float(apache2[i]) - float(apache2[i-1])
        origin.append([train_req/1024000,train_sec/1024000])
      i += 1
  '''

  '''
  while j < thelength1:
      apache1.append(test1[j][key])
      apache21.append(test1[j][key2])
      origin1.append([float(apache1[j])/1024,float(apache21[j])])
      j += 1
  '''
  j = 0

  for item in test1:
    apache1.append(item[u'bytes_recv'])
    apache21.append(item[u'bytes_sent'])
    time_store.append(item[u'time'])
    if j != 0:
      test_req = float(apache1[j]) - float(apache1[j-1])
      test_sec = float(apache21[j]) - float(apache21[j-1])
      origin1.append([test_req/10240,test_sec/10240])
    j += 1

 # train = np.array(origin)
  ceshi = np.array(origin1)
  #print(np.shape(ceshi))

  rng = np.random.RandomState(42)
  clf = IsolationForest(max_samples=300, random_state=rng)
 

  clf.fit(ceshi)  
  anomaly_score = clf.decision_function(ceshi)
  #print(anomaly_score)
 

  bad_domains = []
  out_point1 = []

  threshold = -0.15
  i = 0 
  count = 0 

  for item in anomaly_score:
    if item < threshold:
      bad_domains.append(time_store[i])
      out_point1.append(origin1[i])
      count += 1
    i += 1


  out_point = np.zeros(shape = (len(out_point1),2))
  out_point = np.array(out_point1)
  
  #print(out_point)

  if len(out_point) != 0:

    b2 = plt.scatter(ceshi[:, 0], ceshi[:, 1], c='black',s=20, edgecolor='k')
    b1 = plt.scatter(out_point[:, 0], out_point[:, 1], c='red',s=20, edgecolor='k')
    xx, yy = np.meshgrid(np.linspace(-5, 5, 50), np.linspace(-5, 5, 50))
    Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    

    plt.axis('tight')
    plt.xlim((-500, 500))
    plt.ylim((-500, 500))
   
    plt.legend([b2, b1],
               ["test data",
                "out point"],
               loc="upper left")
  else:
    b2 = plt.scatter(ceshi[:, 0], ceshi[:, 1], c='black',s=20, edgecolor='k')
    xx, yy = np.meshgrid(np.linspace(-5, 5, 50), np.linspace(-5, 5, 50))
    Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    

    plt.axis('tight')
    plt.xlim((-500, 500))
    plt.ylim((-500, 500))
   


  


  filename = 'ioforest'+ str(stamp)+".png"
  #plt.savefig(filename)
  
  
  plt.savefig('maintenanceapp/static/'+filename)
  os.system("cd maintenanceapp/static && python test.py")
  

  

  if len(bad_domains) == 0:
    return jsonify({'count':count,
      'time':bad_domains,
      'filename':filename})
  else:
    return jsonify({'count':count,
        'time':bad_domains,
        'filename': filename})
    



  




  '''
  xx, yy = np.meshgrid(np.linspace(-5, 5, 50), np.linspace(-5, 5, 50))
  Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
  Z = Z.reshape(xx.shape)

  plt.title("IsolationForest")
  plt.contourf(xx, yy, Z, cmap=plt.cm.Blues_r)

  b2 = plt.scatter(ceshi[:, 0], ceshi[:, 1], c='red',
             s=20, edgecolor='k')

  b1 = plt.scatter(train[:, 0], train[:, 1], c='black',
                   s=20, edgecolor='k')

  scores_pred = clf.decision_function(train)
  threshold = stats.scoreatpercentile(scores_pred, )


  plt.contourf(xx, yy, Z, levels=[threshold, Z.max()], colors='palevioletred')
  #a = plt.contour(xx, yy, Z, levels=[threshold], linewidths=2, colors='red')  

  plt.axis('tight')
  plt.xlim((-5, 5))
  plt.ylim((-5, 5))
 
  plt.legend([b1, b2],
             ["training observations",
              "test observations"],
             loc="upper left")





  
  filename = 'ioforest'+ str(stamp)+".png"
  plt.savefig('maintenanceapp/static/'+filename)
 #os.system("cd maintenanceapp/static && python test.py")
  #return filename

  
  image_data = open("maintenanceapp/static/"+filename,"rb").read()
  response = make_response(image_data)
  response.headers['Content-Type'] = 'image/png'
  return response
  '''
