from flask import Flask
from flask import jsonify
from influxdb import InfluxDBClient
from . import routes
from maintenanceapp import *
import time

@routes.route('/cpu')
def log():
    client = InfluxDBClient('localhost',port = 8086,database = 'telegraf')
    num1 = int(time.time())
    num2 = num1 - 60
    str1 = "select * from cpu where time >= " + str(num2) +"s and time <= "+str(num1)+"s"
    temp =  client.query(str1)
    if len(temp) == 0:
        return jsonify({"error code": 416,
      "error message": "Reading data is error"}),416
    
    return jsonify(list(temp)),200
    

    
