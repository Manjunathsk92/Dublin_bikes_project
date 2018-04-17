import flask
from flask import Flask, render_template, request
from flask import jsonify
from main import Main
from flask import g
import sqlalchemy
from sqlalchemy import create_engine
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
 

if __name__ == '__main__':
    app.run(debug=True)
