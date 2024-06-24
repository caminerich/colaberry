from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_restful_swagger import swagger
import sqlite3

app = Flask(__name__)
api = Api(app)

#database path 
db_file = r"/Users/carrieminerich/Desktop/codderry/weather.sqlite"  # Path to SQLite database file

# Function to create a new SQLite connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

# SQL queries for api data
def query_weather(conn):
    sql = """SELECT date, SUBSTR(filename,1,11) as station_id, max_temp_c, min_temp_c, precip
    FROM weather_data
    GROUP BY date, station_id
    order by station_id;"""
    cur = conn.cursor()
    cur.execute(sql)
    weather_data = cur.fetchall()
    return weather_data

def query_stats(conn):
    sql = """SELECT year, weather_station, avg_max_c, avg_min_c, avg_precip
    FROM average
    GROUP BY year, weather_station
    order by weather_station;"""
    cur = conn.cursor()
    cur.execute(sql)
    weather_stats = cur.fetchall()
    return weather_stats

conn = create_connection(db_file)
weather_data = query_weather(conn)
weather_stats = query_stats(conn)
conn.close()

# Example pagination settings
PAGE_SIZE = 10

# Swagger is now OpenAPI; configuration
@app.route('/swagger')
def swagger_docs():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Weather API"
    return jsonify(swag)

# Functions for filtering and pagination
def filter_data(data, date=None, station_id=None, weather_station=None, year=None):
    filtered = data
    
    if date:
        filtered = [item for item in filtered if item['date'] == date]
    
    if station_id:
        filtered = [item for item in filtered if item['station_id'] == station_id]

    if weather_station:
        filtered = [item for item in filtered if item['weather_station'] == weather_station]

    if year:
        filtered = [item for item in filtered if item['year'] == year]
    return filtered

def paginate_data(data, page):
    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    return data[start:end]

# Resource for /api/weather endpoint
class Weather(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('date', type=str, help='Date filter (YYYYMMDD)')
        parser.add_argument('station_id', type=str, help='Station ID filter')
        parser.add_argument('page', type=int, default=1, help='Page number')
        args = parser.parse_args()

        filtered_data = filter_data(weather_data, args['date'], args['station_id'])
        paginated_data = paginate_data(filtered_data, args['page'])

        return jsonify(paginated_data)

# Resource for /api/weather/stats endpoint
class WeatherStats(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('year', type=str, help='Date filter (YYYY)')
        parser.add_argument('weather_station', type=str, help='Weather station ID filter')
        parser.add_argument('page', type=int, default=1, help='Page number')
        args = parser.parse_args()

        filtered_data = filter_data(weather_stats, args['year'], args['weather_station'])
        paginated_data = paginate_data(filtered_data, args['page'])

        return jsonify(paginated_data)

# Add resources to API
api.add_resource(Weather, '/api/weather')
api.add_resource(WeatherStats, '/api/weather/stats')

if __name__ == '__main__':
    app.run(debug=True)
