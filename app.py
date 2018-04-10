import flask
from flask import Flask, render_template, request
from flask import jsonify


app = Flask(__name__)

from views import *

def connect_to_database(URI,PORT,DB,USER,PASSWORD):
 db_str = "mysql+mysqldb://{}:{}@{}:{}/{}"
 engine =create_engine(db_str.format(config.USER,config.PASSWORD,config.URI,config.PORT,config.DB),echo=True)
 return engine


def get_db(URI,PORT,DB,USER,PASSWORD):
 engine = getattr(g, 'engine', None)
 if engine is None:
    engine = g.engine = connect_to_database(URI,PORT,DB,USER,PASSWORD)
 return engine 


@app.route("/stations")
def get_stations():
 engine = get_db('se-project-db.cuph6akhej5q.us-east-2.rds.amazonaws.com','3306','projectdb','Manjunathsk92','Manjunathsk92')
 sql = "select * from station;"
 rows = engine.execute(sql).fetchall()
 print('#found {} stations', len(rows))
 return jsonify(stations=[dict(row.items()) for row in rows]) 

if __name__ == '__main__':
    app.run()
