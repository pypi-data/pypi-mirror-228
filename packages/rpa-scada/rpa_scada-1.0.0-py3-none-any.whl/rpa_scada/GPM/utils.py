from ..common import BaseClient
import pandas as pd
import logging
from datetime import datetime

class GpmUtils():

    def parse_json(
        self,
        data:dict
        )->pd.DataFrame:
        logging.debug("(fnc) GpmClient.parse_json()")

        #---get name columns ---#
        name_columns = {str(series['id']):series['name']+' ('+series['unit']+')' for series in data['series']}
        logging.debug(f" raw column names {name_columns}")

        #---parse data---#
        df = pd.json_normalize(data['data'])
        
        #---replace ids to name ---#
        name_columns = {f'series.{key}.value':value for key,value in name_columns.items()}
        if 'date' in df.columns:
            name_columns['date'] = 'Fecha'
        df = df.rename(columns=name_columns)
        
        #---drop 'medidas' columns---#
        df = df.drop(columns = 'mesure')
        logging.debug(f" New name columns: {df.columns}")
        
        #---fix dtype of date---#
        df['Fecha'] = pd.to_datetime(df['Fecha'],yearfirst=True)
        
        #---drop timezone---#
        df['Fecha'] = df['Fecha'].apply(
            lambda x: x.replace(tzinfo=None)
            )
            
        return df
    
    