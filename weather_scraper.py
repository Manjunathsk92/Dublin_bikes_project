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
cnx = mysql.connector.connect(user='root', password='Anjali123',
                              host='dublinbikes.cbitdsfwlqu1.us-west-2.rds.amazonaws.com',
                             database='mydb')
cursor = cnx.cursor()
print("connect")
insert_data = ("INSERT INTO weather_info "
               "(insert_timestamp, clouds_all, main_humidity, main_pressure, main_temp, main_temp_max, main_temp_min, wind_deg, wind_speed, weather_desc, weather_icon, weather_id, weather_main )"
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

with urllib.request.urlopen("http://api.openweathermap.org/data/2.5/weather?id=7778677&APPID=7eb306b6cee7d8d19ceb36f728b86005") as url:
    print("api")
    data = json.loads(url.read().decode('utf-8'))
print("after api call")
current_time=time.time()
print("length", len(data))
#print(data['weather'][0]['id'])

data_parsed = (current_time, data['clouds']['all'], data['main']['humidity'], data['main']['pressure'], data['main']['temp'], data['main']['temp_max'], data['main']['temp_min'], data['wind']['deg'], data['wind']['speed'], data['weather'][0]['description'], data['weather'][0]['icon'], data['weather'][0]['id'],data['weather'][0]['main'])
print("after data_parsed")
cursor.execute(insert_data, data_parsed)
cnx.commit()

cursor.close()
cnx.close()
print("end")
