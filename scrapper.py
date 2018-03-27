from __future__ import print_function
import sys
sys.path.append("/home/ec2-user/anaconda3/lib/python3.5/site-packages/mysql/connector/__init__.py")
import mysql.connector
import requests
import urllib.request
import json
from pprint import pprint
import ssl
import time
ssl._create_default_https_context = ssl._create_unverified_context
cnx = mysql.connector.connect(user='Manjunathsk92', password='Manjunathsk92',
                              host='se-project-db.cuph6akhej5q.us-east-2.rds.amazonaws.com',
                             database='projectdb')
cursor = cnx.cursor()
print("connect")
insert_data = ("INSERT INTO Dublin_bikes_realtime_week_data "
               "(station_number, station_name, station_address, insert_timestamp,  position_latitude, position_longitude, banking, bonus, status, bike_stands, available_bike_stands, available_bikes, last_update )"
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

with urllib.request.urlopen("https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=afbf7d96c89b1b752484c4f3a1aa7056e323587e") as url:
    print("api")
    data = json.loads(url.read().decode('utf-8'))
print("after api call")
current_time=time.time()
for i in range(len(data)):
    data_parsed = (data[i]['number'], data[i]['name'], data[i]['address'], current_time, data[i]['position']['lat'], data[i]['position']['lng'], data[i]['banking'], data[i]['bonus'], data[i]['status'], data[i]['bike_stands'], data[i]['available_bike_stands'], data[i]['available_bikes'], data[i]['last_update'])
#print("after data_parsed")
    cursor.execute(insert_data, data_parsed)
cnx.commit()

cursor.close()
cnx.close()
print("end")

