from datetime import datetime, time
from typing import Union
import logging
import numpy as np
import pandas as pd
import re
import pytz

from rpa_scada.common import BaseClient

class QantumClient(BaseClient):
    def __init__(
        self,
        user:str,
        pssw:str,
        ssl_path: Union[str, None] = None) -> None:

        super().__init__(ssl_path)

        logging.info('>> Init QANTUM bot...')

        #---URLs & paths---#
        self.LOGIN_URL = 'https://qantum.qosenergy.com/app/auth/'
        self.LOGIN_URL_CHECK = 'https://qantum.qosenergy.com/api/auth/user/login'

        #---credentials---#
        self.USER = user
        self.PASSWORD = pssw

    def login(
        self,
        )->bool:
        logging.info('>> Login')

        logging.debug(' GET login form...')
        response = self.GET(
            url = self.LOGIN_URL,
            header = self.headers,
            )
        
        if response.status_code == 200:

            self.headers['cookie'] = '; '.join([x.name + '=' + x.value for x in response.cookies])
            self.headers['content-type'] = 'application/x-www-form-urlencoded'

            payload = {
                'email': self.USER,
                'password': self.PASSWORD
            }

            logging.debug('  POST credencials... ')
            response = self.POST(
                url = self.LOGIN_URL_CHECK, 
                payload = payload, 
                header = self.headers, 
                )

            logging.debug('  GET cookies...')
            self.headers = {
                'accept': 'application/json, text/plain, */*',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
                }
            self.headers['cookie'] = '; '.join([x.name + '=' + x.value for x in response.cookies])
            logging.debug(f"  cookie: {self.headers['cookie']}")
            return True
        else:
            logging.warning(f"Error when sign in \n response status code: {response.status_code}")
            return False
  
    def get_report(
        self,
        detail:dict,
        start_date:datetime,
        end_date:datetime,
        scale:str='down_scale_15'
        ):

        logging.debug(f"""(fnc) src.rpa.qnt.client.get_report() 
            KWARGS:
            - detail: {detail}
            - start_date: {start_date.strftime('%Y-%m-%d')}
            - end_date: {end_date.strftime('%Y-%m-%d')}
            - scale: {scale}
            """)


        #******WARNING: falta corregir URL_INFO_SENSORES y URL_RAW_DATA pq no cambiamos el id_report 

        # get sensor info
        URL_INFO_SENSORES = 'https://qantum.qosenergy.com/qv3/api_free_period/sensors_data/144103' #-> 144103 es el id_report pero ya no estan los que nos interesan
        date_info = self.get_date_info(start_date,end_date)
        payload = {
            'sensor_ids': ','.join(str(sensor) for sensor in detail['id_sensores']),
            'provider_type': 'SolarField',
            'provider_id': detail['id_planta'],#id_planta
            'period':6, #6: specific date|11:ayer | 0: hoy
            'resolution': scale,
            'yearFrom': date_info['yearFrom'],
            'monthFrom': date_info['monthFrom'],
            'dayFrom': date_info['dayFrom'],
            'tsFrom': date_info['tsFrom'],
            'yearTo': date_info['yearTo'],
            'monthTo': date_info['monthTo'],
            'dayTo': date_info['dayTo'],
            'tsTo': date_info['tsTo']
        }
        logging.info('>> Get data from qantum')
        logging.debug(' >> Get info sensores')

        response_sensores = self.GET(
            url = URL_INFO_SENSORES,
            header=self.headers,
            params=payload
        )
        logging.debug(response_sensores.json())
        
        logging.debug(' >> Get raw data')
        # get raw data
        URL_RAW_DATA = 'https://qantum.qosenergy.com/qv3/api_free_period/raw_values/144103'
        response_raw_data = self.GET(
            url = URL_RAW_DATA,
            header=self.headers,
            params=payload
        )
        logging.debug(response_raw_data.json())
        if response_raw_data.status_code == 200 and response_sensores.status_code==200:

            return self.parse_response(
                columns = response_sensores.json(),
                data = response_raw_data.json(),
                patterns=detail['patterns']
            )
        
        else:
            logging.info(f"""Error when get data from qantum because response codes are:
                - info sensores: {response_sensores.status_code}
                - raw data : {response_raw_data.status_code}""")
            logging.warning(f"Return None data from qantum")
            return None

    """ UTILS """

    def get_date_info(
        self,
        start_date:datetime,
        end_date:datetime,
        ):

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

    """ Utils to parse response"""
    def get_col_names(
        self,
        data:list[dict]
        )-> dict:
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
        patterns):
        logging.debug("(fnc) src.rpa.utils.rename_columns()")
        map_names = {} 
        for col_name in list_columns:
            new_name = self.find_pattern(col_name,patterns)
            if new_name is not None:
                # se agrego aleta en find_pattern()
                map_names[col_name] = new_name
        
        return map_names

    def find_pattern (
        self,
        col_name,
        patterns):
        for pat in patterns:
            if re.search(pat[0],col_name):
                return pat[1]
        
        logging.warning(f"Dont find pattern to column: {col_name}")
        return None

    def fix_columns(
        self,
        df:pd.DataFrame,
        columns:list):

        for col in columns:
            if col not in df.columns:
                logging.warning(f" * Empty column:{col}")
                df[col]=np.nan
        
        return df[columns]

    def parse_response(
        self,
        columns:list[dict],
        data:list,
        patterns:list
        )->pd.DataFrame:
        logging.debug("(fnc) src.rpa.utils.parse_response()")
        logging.info(">> Parse data response from Qantum")

        logging.debug(' >> Create Df from Qantum response')
        columns=self.get_col_names(data=columns)
        data = np.array(data)

        df = pd.DataFrame(
            np.append(data[0,:,:],data[1:,:,1].T,axis=1),
            columns=['Fecha']+[col['name'] for _,col in columns.items()]
            )

        logging.debug(' >> Fix timestamp')
        df['Fecha'] = df['Fecha'].apply(
            lambda x: pd.Timestamp(
                x,
                unit='s',
                tzinfo=pytz.timezone('America/Santiago')
                ).replace(tzinfo=None)
            )
        logging.debug(' >> Rename columns')
        df = df.rename(columns = self.rename_columns(df.columns,patterns))
        # df = self.fix_columns(df,[col for _,col in patterns])
        df = df.fillna(value=np.nan)
        return df