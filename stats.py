import sqlite3

# Function to create a new SQLite connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

# Function to create a new table in the SQLite database
def create_table(conn, create_table_sql):
    try:
        cur = conn.cursor()
        cur.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

# Function to insert a new row of data into the SQLite table
def insert_avg_data(conn, year, weather_station, avg_precip, avg_max_c, avg_min_c ):
    sql = '''INSERT INTO average(year, weather_station, avg_precip, avg_max_c, avg_min_c )
            VALUES(?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, (year, weather_station, avg_precip, avg_max_c, avg_min_c))
    print(f"inserted into average table year {year} weather_station {weather_station}")
    conn.commit()
    return cur.lastrowid

def query_average(conn):
    sql = """SELECT substr(date, 1, 4) AS year, 
    substr(filename, 1, 7) AS weather_station, 
    AVG(precip) AS avg_precip,
    AVG(max_temp_c) as avg_max_c,
    AVG(max_temp_f) as avg_min_c
    FROM weather_data
    where precip != '-9999' and max_temp_c != '-9999' and max_temp_f != '-9999'
    GROUP BY year, weather_station
    order by weather_station;"""
    # print(sql)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    results = cur.fetchall()
    for row in results:
        year, weather_station, avg_precip, avg_max_c, avg_min_c = row
        insert_avg_data(conn, year, weather_station, avg_precip, avg_max_c, avg_min_c)
    
      
def main():
    database = r"/Users/carrieminerich/Desktop/codderry/weather.sqlite"  # Path to SQLite database file
    # averages for each year, each weather station 
    sql_create_table = """CREATE TABLE IF NOT EXISTS average(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year TEXT NOT NULL,
        weather_station INTEGER,
        avg_precip FLOAT NOT NULL,
        avg_max_c FLOAT NOT NULL,
        avg_min_c FLOAT NOT NULL); """

    # Create a database connection
    conn = create_connection(database)

    if conn is not None:
        # Create sql table
        create_table(conn, sql_create_table)

        query_average(conn)
        # Close the database connection
        conn.close()
    
    
if __name__ == '__main__':
    main()