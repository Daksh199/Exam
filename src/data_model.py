

import os
import pandas as pd
import sqlite3

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "{}".format(os.path.join(project_dir, "weatherrecords_database.db"))


class WeatherDataModel():
    def __init__(self):
       
        self.db_name = 'weather_records'
        

        self.db = sqlite3.connect(database_file)
        self.cur = self.db.cursor()
        self.cur.execute(f'''CREATE TABLE IF NOT EXISTS {self.db_name} (
                        StationID TEXT(15),
                        Date TEXT(10),
                        MaxTemp INTEGER,
                        MinTemp INTEGER,
                        Precipitation INTEGER
                        );''')
    def add_entry(self, record):
       
        self.cur = self.db.cursor()
        if len(list(self.cur.execute(f'select * from {self.db_name} where StationID="{record[0]}" and Date={record[1]}'))):
            return 0
        self.cur.execute(f"insert into {self.db_name}  (StationID, Date, MaxTemp, MinTemp, Precipitation) values{record};")
        self.db.commit()
        return 1

    def get_data(self, query=None):
        
        if query:
            return pd.read_sql(f'select * from {self.db_name} where StationID="{query[0]}" and Date={query[1]}', self.db)
        return pd.read_sql(f'select *  from {self.db_name}', self.db)


class WeatherStatsDataModel():
    def __init__(self):
       
        self.db_name = 'weatherstats'
        print('Connecting to DB')
        self.db = sqlite3.connect(database_file)
        self.cur = self.db.cursor()
        self.cur.execute(f'''CREATE TABLE IF NOT EXISTS {self.db_name} (
                        StationID TEXT(15),
                        Year TEXT(5),
                        AvgMaxTemp FLOAT,
                        AvgMinTemp FLOAT,
                        TotalPrecipitation FLOAT
                        );''')
        print('Table created successfully')

    def add_entry(self, record):
        
        self.cur = self.db.cursor()
        if len(list(self.cur.execute(f'select * from {self.db_name} where StationID="{record[0]}" and Year={record[1]}'))):
            return 0
        self.cur.execute(f"insert into {self.db_name}  (StationID, Year, AvgMaxTemp, AvgMinTemp, TotalPrecipitation) values{record};")
        self.db.commit()
        return 1

    def get_data(self, query=None):
        
        if query:
            return pd.read_sql(f'select * from {self.db_name} where StationID="{query[0]}"', self.db)
        return pd.read_sql(f'select *  from {self.db_name}', self.db)
