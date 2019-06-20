
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





@routes.route('/image/<float:stamp>')
def get_image(stamp):
    client = InfluxDBClient('localhost',port = 8086,database = 'telegraf');

   # stamp = time.time()  
    num1 = int(stamp)
    num2 = num1 - 300
    str1 = 'select "usage_idle" , "usage_iowait" from cpu where time >= '+ str(num2) +'s and time <= '+str(num1)+'s'


    

    temp = client.query(str1)
    points = temp.get_points()
    if len(temp) == 0:
        return jsonify({"error code": 416,
      "error message": "Reading data is error"}),416

    ax1 = array('f')
    #ax2 = np.linspace(stamp-300,stamp,num=150)
    #ax3 = [time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(d)) for d in ax2]

    count = 0
    for items in points:
        ax1.append(items[u'usage_idle'])
        count += 1
        ax2 = np.linspace(stamp-300,stamp,num=count)
    ax3 = [time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(d)) for d in ax2]

     


    tick_spacing = 40
    fig,ax = plt.subplots(1,1)
    ax.plot(ax3,ax1)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    plt.xticks(rotation=20)
    plt.xticks(fontsize = 10)
    plt.title("usage_idle")
    plt.subplots_adjust(bottom = 0.2)
    filename = 'cpu'+str(num1)+".png"

    plt.savefig('maintenanceapp/static/'+filename)
    os.system("cd maintenanceapp/static && python test.py")
      
    '''
    image_data = open("maintenanceapp/static/"+filename,"rb").read()
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/png'
    print(type(response))
    return response
    '''
    #return jsonify(filename)
    return filename
'''
msg_handle = threading.Thread(target=get_image, args=(stamp,))
msg_handle.daemon = True
msg_handle.start()
'''
