# colaberry
Colaberry Data Engineer Challenge

### open_and_parse.py
- This script creates a SQLite table called "weather_data" and ingests TXT weather station files from local machine
- This script also creates a SQLite table called "transaction_log" that records the start, end, and duration time of each record as it is ingested into the 'weather_data' table
- Must change database path and file path to your project requirements

### stats.py
- This script creates an 'average' table with pre-calculated average max C temp, average min C temp, and average precip for each year and each weather station.

### app.py
- This script is a flask web framework to publish data to two API endpoints:
    - /api/weather
    - api/weather/stats
- The ends points provide a searchable feature for date and weather station
- Swagger documentation 

### Additional Documentation
- Weather stations data dates are between 1985-01-01 to 2014-12-31
- Weather station states are the first 7 letters of the filename (ie USC00025) and correspond to Nebraska, Iowa, Illinois, Indiana, or Ohio
- Testing files, labeled "test" with .TXT extension, provided to test code without ingesting large amounts of data. Remember to DROP TABLE before ingesting production data as data will not overright. 

### Future Improvements 
- Implement more robust unit testing
- Concurrency or other means to increase speed that raw weather TXT data is ingested in SQLlite database 
- Flask API is vulnerable code, not providing the searchable web interface and error with swagger documentation 
