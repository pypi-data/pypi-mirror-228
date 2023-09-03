from datetime import datetime, time
from typing import Union
import pandas as pd
import numpy as np
import logging
import pytz
import re

class QantumUtils():
    def __init__(self) -> None:
        pass
    
    def get_date_info(
        self,
        start_date:datetime,
        end_date:datetime,
        ) -> dict:
        """
        Parse dict from datetimes to set payload that we use on request
        """
        logging.debug("(fnc) src.rpa.QantumClient.get_date_info()")
        start_date = datetime.combine(start_date,time=time(0,0,0))
        end_date = datetime.combine(end_date,time=time(23,59,59))

        return {
            'yearFrom':start_date.year,
            'monthFrom':start_date.month,
            'dayFrom':start_date.day,
            'tsFrom':start_date.timestamp(),
            'yearTo':end_date.year,
            'monthTo':end_date.month,
            'dayTo':end_date.day,
            'tsTo':end_date.timestamp()
        }

    def get_col_names(
        self,
        data:list[dict]
        )-> dict:
        """
        DESCIPTION:
            Method to handle and order column names of request
        
        INPUT:
            List of dict, each dict has information of one sensor
        
        RETURN:
            Dict with parsed information of all sensors 
        
        """
        logging.debug("(fnc) src.rpa.utils.get_col_names()")
        result = {
            int(sensor['sensorId']) : {
                'name' :sensor['main_provider']['name']+ ' - '+ sensor['provider']['name']+' - '+sensor['name']+ ' - ' + sensor['unit'],
                'unit' : sensor['unit'],
                'timezone':sensor['timezoneIdentifier']
            } for sensor in data
        }
        return result
     
    def rename_columns(
        self,
        list_columns,
        patterns
        ) -> dict:
        """
        Create dict with new names of columns, if dont find, delete column (?)
        """
        logging.debug("(fnc) src.rpa.utils.rename_columns()")
        map_names = {} 
        for col_name in list_columns:
            new_name = self.find_pattern(col_name,patterns)
            if new_name is not None:
                map_names[col_name] = new_name
        
        return map_names

    def find_pattern (
        self,
        col_name,
        patterns
        ) -> Union[str,None]:
        """
        find pattern by column to standarize tables
        """
        for pat in patterns:
            if re.search(pat[0],col_name):
                return pat[1]
        
        logging.warning(f"Dont find pattern to column: {col_name}")
        return None

    def fix_columns(
        self,
        df:pd.DataFrame,
        columns:list
        ) -> pd.DataFrame:
        """
        Add NaN values if response has not column
        """
        for col in columns:
            if col not in df.columns:
                logging.warning(f" * Empty column:{col}")
                df[col]=np.nan
        
        return df[columns]
    
    def set_dataframe(
        self,
        columns:list[dict],
        data:list,
        )->pd.DataFrame:
        """
        Create Dataframe and set timestamp that 'Fecha' column
        """

        logging.debug('Create DataFrame')
        df = pd.DataFrame(
            np.append(data[0,:,:],data[1:,:,1].T,axis=1),
            columns=['Fecha']+[col['name'] for _,col in columns.items()]
            )

        logging.debug('Fix timestamp')
        df['Fecha'] = df['Fecha'].apply(
            lambda x: pd.Timestamp(
                x,
                unit='s',
                tzinfo=pytz.timezone('America/Santiago')
                ).replace(tzinfo=None)
            )
        
        return df
    
    def parse_response(
        self,
        df:pd.DataFrame,
        patterns:list
        )->pd.DataFrame:
        """
        Create Dataframe and apply several methods to insert into SQL
        """
        logging.info(">> Parse data response from Qantum")

        logging.debug('Rename columns')
        df = df.rename(columns = self.rename_columns(df.columns,patterns))
        df = self.fix_columns(df,[col for _,col in patterns])
        df = df.fillna(value=np.nan)
        
        return df