from flask import Flask, render_template, request
from flask import jsonify
from flask_cors import cross_origin

import services

app = Flask(__name__)

#app.add_url_rule('/',
                 #view_func=Main.as_view('main'),
                 #methods=["GET"])
#print("Hi am her2");
#app.add_url_rule('/<page>/',
                # view_func=Main.as_view('page'),
                # methods=["GET"])

@app.route('/')
def main():
    return render_template("index.html")

@app.route("/stations")
def get_stations():
 engine = services.get_db('se-project-db.cuph6akhej5q.us-east-2.rds.amazonaws.com', '3306', 'projectdb', 'Manjunathsk92', 'Manjunathsk92')
 sql = "SELECT distinct station_name,station_number,station_address,position_latitude,position_longitude FROM projectdb.Dublin_bikes_realtime_week_data;"
 rows = engine.execute(sql).fetchall()
 print('#found {} stations', len(rows))
 return jsonify(stations=[dict(row.items()) for row in rows])

@app.route('/charts_daily', methods=['GET', 'POST'])
@cross_origin()
def get_charts_daily():
    """Gets the average number of bikes and stands for each day"""
    station_number = request.args.get('station_number')
    type = request.args.get('type')
    return services.daily_avg_dynamic(station_number, type)

if __name__ == '__main__':
    app.run()
