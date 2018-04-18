import flask
from flask import Flask, render_template, request
from flask import jsonify
from main import Main
from flask import g
import sqlalchemy
from sqlalchemy import create_engine,text
import mysql.connector
app = Flask(__name__)

#app.add_url_rule('/',
                 #view_func=Main.as_view('main'),
                 #methods=["GET"])
#print("Hi am her2");
#app.add_url_rule('/<page>/',
                # view_func=Main.as_view('page'),
                # methods=["GET"])

def connect_to_database(URI,PORT,DB,USER,PASSWORD):
 db_str = "mysql+pymysql://{}:{}@{}:{}/{}"
 engine =create_engine(db_str.format(USER,PASSWORD,URI,PORT,DB),echo=True)
 return engine


def get_db(URI,PORT,DB,USER,PASSWORD):
 engine = getattr(g, 'engine', None)
 if engine is None:
    engine = g.engine = connect_to_database(URI,PORT,DB,USER,PASSWORD)
 return engine 

@app.route('/')
def main():
    return render_template("index.html")

@app.route("/stations")
def get_stations():
 engine = get_db('se-project-db.cuph6akhej5q.us-east-2.rds.amazonaws.com','3306','projectdb','Manjunathsk92','Manjunathsk92')
 sql="select station_name,station_number,station_address,position_latitude,position_longitude,banking,bike_stands,available_bike_stands,available_bikes from projectdb.dublin_bikes_current_data";
 #sql = "SELECT distinct station_name,station_number,station_address,position_latitude,position_longitude FROM projectdb.Dublin_bikes_realtime_week_data;"
 #sql="SELECT station_number,station_name,station_address,banking,bike_stands,available_bike_stands, available_bikes, substring(from_unixtime(insert_timestamp),1,16) FROM  projectdb.Dublin_bikes_realtime_week_data where insert_timestamp<=(select max(insert_timestamp) from projectdb.Dublin_bikes_realtime_week_data) and insert_timestamp>= (select max(insert_timestamp)-10 from  projectdb.Dublin_bikes_realtime_week_data) group by station_number;"
 rows = engine.execute(sql).fetchall()
 print('#found {} stations', len(rows))
 return jsonify(stations=[dict(row.items()) for row in rows])

'''@app.route("/availability")
#@cross_origin()
def availability():
    engine = get_db('se-project-db.cuph6akhej5q.us-east-2.rds.amazonaws.com','3306','projectdb','Manjunathsk92','Manjunathsk92')
    # change this to suit what queries we will be using
    sql="select station_name,station_number,station_address,position_latitude,position_longitude,banking,bike_stands,available_bike_stands,available_bikes from projectdb.dublin_bikes_current_data";
    rows = engine.execute(sql).fetchall()
    print("#found {} availability", len(rows))
    availability = jsonify(stations=[dict(row) for row in rows])
    engine.dispose()
    return availability'''

@app.route('/station_details', methods=['GET', 'POST'])
#@cross_origin()
def station_details():
    """Function to get dyanmic details for stations"""
    #Info will be pulled from a javascript function on the home page
    station_number = request.args.get('station_number')
    engine = get_db('se-project-db.cuph6akhej5q.us-east-2.rds.amazonaws.com','3306','projectdb','Manjunathsk92','Manjunathsk92')
    sql = "select station_name,station_number,station_address,position_latitude,position_longitude,banking,bike_stands,available_bike_stands,available_bikes from projectdb.dublin_bikes_current_data where station_number=%s";
    rows = engine.execute(sql, station_number).fetchall()
    print("#found {} stations", len(rows))
    return jsonify(stations=[dict(row.items()) for row in rows])
 

@app.route('/charts_daily', methods=['GET', 'POST'])
def get_charts_daily():
    """Gets the average number of bikes and stands for each day"""
    station_number = request.args.get('station_number')
 #   date_time=request.args.get('date_time')
#    print(date_time)
    type = request.args.get('type')
    return daily_avg_dynamic(station_number, type)

def daily_avg_dynamic(station_number, type='daily'):
    """Returns the average number of bike per day"""
    st_num = int(station_number)
    engine = get_db('se-project-db.cuph6akhej5q.us-east-2.rds.amazonaws.com', '3306', 'projectdb', 'Manjunathsk92',
                    'Manjunathsk92')
    if type == 'daily':
        sql = text("SELECT AVG(available_bikes) as avg_bikes, AVG(available_bike_stands) as avg_stands, station_number, DATE_FORMAT(FROM_UNIXTIME(`insert_timestamp`), '%e %b %Y') AS 'date_formatted' FROM Dublin_bikes_realtime_week_data WHERE insert_timestamp >= unix_timestamp(curdate() - INTERVAL DAYOFWEEK(curdate())+6 DAY) AND insert_timestamp < unix_timestamp(curdate() - INTERVAL DAYOFWEEK(curdate())-1 DAY) and station_number = " + str(st_num) +" group by date_formatted order by insert_timestamp asc;")
    else:
        sql = text("SELECT AVG( available_bikes ) as avg_bikes, AVG(available_bike_stands) as avg_stands, substring(from_unixtime(insert_timestamp),12,2) AS 'date_formatted' FROM Dublin_bikes_realtime_week_data where insert_timestamp < unix_timestamp(curdate() - 1) and insert_timestamp > unix_timestamp(curdate() - 2) and station_number = "+ str(st_num) +" GROUP by date_formatted ;")
    results = engine.execute(sql).fetchall()
    engine.dispose()
    print('#found {} stations', len(results))
    return jsonify(stations=[dict(row.items()) for row in results])

@app.route('/predicted_value', methods=['GET', 'POST'])
def prediction_linear_reg():
    station_number=int(request.args.get('station_number'))
    date_time=request.args.get('date_time')
    hire_or_return=request.args.get('hire_or_return')
    
    import pandas as pd
    import mysql.connector
    import numpy as np
    import statsmodels.formula.api as sm
    import requests
    import urllib.request
    import json
    from pprint import pprint

    pd.options.display.max_rows = 8000
    pd.options.display.max_columns = 100


    #station_number=1
    #date_time="2018-04-18 16"
    if len(date_time)==13:
        hour=date_time[11:14]
        time_validation=int(date_time[11:14])
    else:
        hour=date_time[11:13]
        time_validation=int(date_time[11:13])
    correction_value=time_validation%3
    if correction_value==1:
        new_hour=time_validation-1
    elif correction_value==2:
        new_hour=time_validation+1
    else :
        new_hour=time_validation
    if new_hour==24:
        new_hour=21
    date_time=date_time[:11] + str(new_hour)

    with urllib.request.urlopen("http://api.openweathermap.org/data/2.5/forecast?id=7778677&APPID=a333fd4b6cc086808ce5e483c98b85f6") as url:
        data = json.loads(url.read().decode('utf-8'))
    list_index=0
    for i in range (len(data['list'])):
        if data['list'][i]['dt_txt'][:13]==date_time:
            list_index=i
            break
    temp=data['list'][list_index]['main']['temp']
    weather_desc=data['list'][list_index]['weather'][0]['description']
    weather_main=data['list'][list_index]['weather'][0]['main']




    db_connection = mysql.connector.connect(user='Manjunathsk92', password='Manjunathsk92',
                                  host='se-project-db.cuph6akhej5q.us-east-2.rds.amazonaws.com',
                                 database='projectdb')
 #   db_cursor = db_connection.cursor()

    wd_connection = mysql.connector.connect(user='root', password='Anjali123',
                                  host='dublinbikes.cbitdsfwlqu1.us-west-2.rds.amazonaws.com',
                                 database='mydb')
#    wd_cursor = wd_connection.cursor()

 #   day='Wednesday'
    dbikes = pd.read_sql('SELECT station_number, insert_timestamp, bike_stands, available_bike_stands, available_bikes, substring(from_unixtime(floor(insert_timestamp)),1,13) as date, from_unixtime(floor(insert_timestamp), "%H") as hour, dayname(from_unixtime(insert_timestamp)) as day_of_week FROM projectdb.Dublin_bikes_realtime_week_data where station_number=%(station_number)s ', con=db_connection, params={'station_number':station_number} )

    wdata = pd.read_sql('SELECT substring(from_unixtime(floor(insert_timestamp)),1,13) as date, main_temp, weather_desc, weather_main FROM mydb.weather_info ', con=wd_connection)
    ata=wdata.drop_duplicates(subset='date')
    total_bike_stands=int(dbikes['bike_stands'][1])

    dbikes['date']=dbikes['date'].astype('object')

    wdata['date']=wdata['date'].astype('object')

    dbikes_weather=dbikes.join(wdata.set_index('date'),on ='date')
    dbikes_weather['available_bikes']=dbikes_weather['available_bikes'].astype('int')


    dbikes_weather = dbikes_weather[np.isfinite(dbikes_weather['main_temp'])]
    dbikes_weather.reset_index(inplace=True)

    lm=sm.ols(formula="available_bikes ~ main_temp + C(hour) + C(weather_desc) + C(weather_main)", data=dbikes_weather).fit()
    print("beofre lm")
    df_new=pd.DataFrame({'main_temp': [temp], 'hour': [hour], 'weather_desc': [weather_desc], 'weather_main':[weather_main]})


    bike_prediction=int(lm.predict(df_new))
    print("bikes", bike_prediction)
    print("stands", total_bike_stands)
    if hire_or_return == "return" :
        return str(total_bike_stands - bike_prediction)       
    return str(bike_prediction)


if __name__ == '__main__':
    app.run(debug=True)
