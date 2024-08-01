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

# Function to insert a new row of data into the statistics table
def insert_stats_data(conn, year, weather_station, avg_max_temp_c, avg_min_temp_c, total_precip_cm):
    sql = '''INSERT INTO weather_stats(year, weather_station, avg_max_temp_c, avg_min_temp_c, total_precip_cm)
            VALUES(?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, (year, weather_station, avg_max_temp_c, avg_min_temp_c, total_precip_cm))
    conn.commit()
    return cur.lastrowid

# Main function to create database and calculate statistics
def main():
    database = r"//Users//carrieminerich//Desktop//codderry//weather.db"

    sql_create_stats_table = """
    CREATE TABLE IF NOT EXISTS weather_stats (
        id INTEGER PRIMARY KEY,
        year TEXT NOT NULL,
        weather_station TEXT NOT NULL,
        avg_max_temp_c REAL,
        avg_min_temp_c REAL,
        total_precip_cm REAL
    );"""

    # Create a database connection
    conn = create_connection(database)

    if conn is not None:
        # Create the statistics table
        create_table(conn, sql_create_stats_table)
    else:
        print("Error! Cannot create the database connection.")
        return

    # SQL query to calculate the required statistics
    sql_query_stats = """
    SELECT 
        substr(date, 1, 4) AS year, 
        substr(filename, 1, 7) AS weather_station, 
        ROUND(AVG(CASE WHEN max_temp_c != -9999 THEN max_temp_c / 10.0 ELSE NULL END), 2) AS avg_max_temp_c,
        ROUND(AVG(CASE WHEN min_temp_c != -9999 THEN min_temp_c / 10.0 ELSE NULL END), 2) AS avg_min_temp_c,
        ROUND(SUM(CASE WHEN precip != -9999 THEN precip ELSE 0 END) / 100.0, 2) AS total_precip_cm
    FROM weather_data
    GROUP BY year, weather_station;
    """

    try:
        cur = conn.cursor()
        cur.execute(sql_query_stats)
        rows = cur.fetchall()

        for row in rows:
            year, weather_station, avg_max_temp_c, avg_min_temp_c, total_precip_cm = row
            insert_stats_data(conn, year, weather_station, avg_max_temp_c, avg_min_temp_c, total_precip_cm)

    except sqlite3.Error as e:
        print(e)

    # Close the connection
    if conn:
        conn.close()

if __name__ == '__main__':
    main()
