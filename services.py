from flask import jsonify
from sqlalchemy import create_engine, text

def connect_to_database(URI,PORT,DB,USER,PASSWORD):
 db_str = "mysql+pymysql://{}:{}@{}:{}/{}"
 engine =create_engine(db_str.format(USER,PASSWORD,URI,PORT,DB),echo=True)
 return engine


def get_db(URI, PORT ,DB, USER, PASSWORD):
 # engine = getattr(g, 'engine', None)
 # if engine is None:
    engine = connect_to_database(URI,PORT,DB,USER,PASSWORD)
    return engine


def daily_avg_dynamic(station_number, type='daily'):
    """Returns the average number of bike per day"""

    st_num = int(station_number)
    engine = get_db('se-project-db.cuph6akhej5q.us-east-2.rds.amazonaws.com', '3306', 'projectdb', 'Manjunathsk92',
                    'Manjunathsk92')
    if type == 'daily':
        sql = text("SELECT AVG(available_bikes) as avg_bikes, AVG(available_bike_stands) as avg_stands, station_number, DATE_FORMAT(FROM_UNIXTIME(`insert_timestamp`), '%e %b %Y') AS 'date_formatted' FROM Dublin_bikes_realtime_week_data WHERE insert_timestamp >= unix_timestamp(curdate() - INTERVAL DAYOFWEEK(curdate())+6 DAY) AND insert_timestamp < unix_timestamp(curdate() - INTERVAL DAYOFWEEK(curdate())-1 DAY) and station_number = " + str(st_num) +" group by date_formatted order by insert_timestamp asc;")
    else:
        sql = text("SELECT AVG( available_bikes ) as avg_bikes, AVG(available_bike_stands) as avg_stands, from_unixtime(insert_timestamp) AS 'date_formatted' FROM Dublin_bikes_realtime_week_data where insert_timestamp < unix_timestamp(curdate() - 1) and insert_timestamp > unix_timestamp(curdate() - 2) and station_number = "+ str(st_num) +" GROUP BY DATE( date_formatted ), HOUR( date_formatted );")
    results = engine.execute(sql).fetchall()


    engine.dispose()
    print('#found {} stations', len(results))
    return jsonify(stations=[dict(row.items()) for row in results])

