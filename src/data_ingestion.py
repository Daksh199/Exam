

import os
import pandas as pd
import datetime
from data_model import WeatherDataModel


datamodel = WeatherDataModel()


def data_ingestion():
   
    
    files = os.listdir('../wx_data')
    counter = 0 
    for filename in files:
        
        data = pd.read_csv(f'../wx_data/{filename}', sep='\t', header=None,
                           names=['Date', 'MaxTemp', 'MinTemp', 'Precipitation'])
        
        data.fillna(-9999)
       
        data['StationID'] = filename.replace('.txt', '')
        data = data[['StationID', 'Date', 'MaxTemp', 'MinTemp', 'Precipitation']]

     
        data.drop_duplicates(subset=['Date'], inplace=True)

      
        for index, record in data.iterrows():
            counter += datamodel.add_entry(tuple(record))

    print(f'End Time:{datetime.datetime.now()}')
    print('Total Records inserted: ', counter)


if __name__ == '__main__':
    data_ingestion()
