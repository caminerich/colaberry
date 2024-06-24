import sqlite3
import os
import time

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
def insert_data(conn, date, max_temp_c, min_temp_c, precip, filename):
    sql = '''INSERT INTO weather_data(date, max_temp_c, min_temp_c, precip, filename)
            VALUES(?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, (date, max_temp_c, min_temp_c, precip, filename))
    conn.commit()
    return cur.lastrowid

def query_row_count(conn, filename):
    sql = f'''SELECT COUNT(*) FROM weather_data WHERE filename = '{filename}'; '''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    result = cur.fetchone()
    record_count = str(result[0])
    print(f"Row count for {filename} is {record_count} records")
    return record_count

# Function to insert log transactions into SQLite table
def log_transaction(conn, start_time, end_time, duration, record_count, filename):
    try:
        sql = '''
            INSERT INTO transaction_log (start_time, end_time, duration, record_count, filename) 
            VALUES (?,?,?,?,?)
        '''
        cur = conn.cursor()
        cur.execute(sql, (start_time, end_time, duration, record_count, filename))
        conn.commit()
        print(f"Transaction logged successfully: {filename}, {record_count} records in {duration} time")

    except sqlite3.Error as e:
        print(f"Error logging transaction: {e}")


# Main function to parse text files and insert data into SQLite
# Your code should also produce log output indicating start and end times and number of records ingested.
def main():
    database = r"/Users/carrieminerich/Desktop/codderry/weather.sqlite"  # Path to SQLite database file
    sql_create_table = """CREATE TABLE IF NOT EXISTS weather_data(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        max_temp_c REAL,
        min_temp_c REAL, 
        precip REAL,
        filename TEXT NOT NULL); """

    sql_log = """
    CREATE TABLE IF NOT EXISTS transaction_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
        start_time TEXT,
        end_time TEXT,
        duration REAL,
        record_count INTEGER,
        filename TEXT NOT NULL
    );"""    

    # Create a database connection
    conn = create_connection(database)

    if conn is not None:
        # Create sql table
        create_table(conn, sql_create_table)
        create_table(conn, sql_log)

        # Directory containing text files
        directory = r'//Users//carrieminerich//Desktop//codderry//code-challenge-template//wx_data'
        # test file
        #directory = r'//Users//carrieminerich//Desktop//codderry//test'

        # Iterate through all files in the directory
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                filepath = os.path.join(directory, filename)
                print(filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    for line in file:
                        # Split line by whitespace
                        parts = line.split()
                        if len(parts) == 4:
                            date = parts[0]
                            max_temp_c = float(parts[1])
                            min_temp_c = float(parts[2])
                            precip = float(parts[3])
                            filename = filename
                            start_time = time.time()
                            insert_data(conn, date, max_temp_c, min_temp_c, precip, filename)
                            #print(f"Inserted data from {filename} into SQLite")
                        end_time = time.time()

                duration = end_time - start_time
                #print(record_count)
                record_count = query_row_count(conn, filename)
                log_transaction(conn, start_time, end_time, duration, record_count, filename)

        # Close the database connection
        conn.close()
    else:
        print("Error! Cannot create the database connection.")

    


if __name__ == '__main__':
    main()