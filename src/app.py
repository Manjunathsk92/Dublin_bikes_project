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
 sql = "SELECT distinct station_name FROM projectdb.Dublin_bikes_realtime_week_data;"
 rows = engine.execute(sql).fetchall()
 print('#found {} stations', len(rows))
 return jsonify(stations=[dict(row.items()) for row in rows]) 

if __name__ == '__main__':
    app.run()
