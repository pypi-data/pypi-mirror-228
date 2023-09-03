import logging
from typing import Union
from .auth import QantumAuth
from .utils import QantumUtils
from datetime import datetime
import numpy as np
import pandas as pd

class QantumReports(
    QantumAuth, # esta clase tiene preferencia en el MRO (Method Resolution Order)
    QantumUtils
    ):
    
    def __init__(
        self, 
        # QantumAuth parameters
        user: str, 
        pssw: str, 
        ssl_path: Union[str, None] = None
        ) -> None :
        """
        DESCRIPTION
            BOT to get and parse information from Qantum SCADA
        """
        super().__init__(user, pssw, ssl_path)
        
        #--- Extra paths ---#
        self.INFO_SENSORS_PATH = '/qv3/api_free_period/sensors_data'
        self.RAW_VALUES_PATH = '/qv3/api_free_period/raw_values'
        self.DEFAULT_ID_REPORT = '/144103'

        self.login_status = self.login()

    def set_payload_report(
        self,
        detail:dict,
        start_date:datetime,
        end_date:datetime,
        scale:str='down_scale_15'
        ) -> dict:
        """
        Parse params to set payload
        """
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
        return payload

    def get_info_sensors(
        self,
        payload: dict,
        ) -> dict:
        """
        Get information about sensors
        """
        logging.debug('Get informations about sensors')
        URL = self.BASE_URL + self.INFO_SENSORS_PATH +  self.DEFAULT_ID_REPORT
        response = self.GET(
            url = URL,
            header=self.session.headers,
            params=payload
        )
        if response.status_code == 200:
            logging.debug('Response code: 200')
            
            # parse columns names
            columns = self.get_col_names(data=response.json()) 
        else:
            logging.warning('NO response info sensors, return empty dict')
            columns = {}
        
        return columns
        
    def get_raw_values_sensors(
        self,
        payload:dict
        ) -> np.array:
        """
        Get data from sensors
        """
        URL = self.BASE_URL + self.RAW_VALUES_PATH + self.DEFAULT_ID_REPORT
        response = self.GET(
            url = URL,
            header=self.session.headers,
            params=payload
        )
        if response.status_code == 200:
            data = np.array(response.json())
        else:
            logging.warning('NO response raw values sensors, return empty array')
            data = np.array([])

        return data
       
    def get_raw_report(
        self,
        detail:dict,
        start_date:datetime,
        end_date:datetime,
        scale:str='down_scale_15'
        )->Union[pd.DataFrame,None]:
        """
        DESCRIPTION
            Metodo que hace 2 consultas (informacion de sensores y valor de sensores) para retornar un dataframe con los datos solicitados desde qantum
        
        INPUT
        * detail: diccionario con la informacion de la planta
        * start_date: datetime que indica el inicio de la consulta desde las 00:00
        * end_date: datetime indica el fin de la consula a las 23:59
        * scale: Sting que indica la temporalidad de los registros, por default esta en 15 minutos

        RETURN
        * Dataframe -> si se ejecutó correctamente la consulta
        * None -> en caso de cualquier error

        """
        payload = self.set_payload_report(
            detail=detail,
            start_date=start_date,
            end_date=end_date,
            scale=scale
        )  
        # logging.debug(f"PAYLOAD: {payload}")
        columns = self.get_info_sensors(payload=payload)
        # logging.debug(f"COLUMNS: {columns}")
        data = self.get_raw_values_sensors(payload=payload)
        # logging.debug(f"data: {data}")

        if columns == {}:
            # no se obtuvo una respuesta correcta desde qantum
            logging.warning(f"Return None data from qantum")
            return None
        
        if data.size == 0:
            # no se obtuvo una respuesta correcta desde qantum
            logging.warning(f"Return None data from qantum")
            return None
        
        df = self.set_dataframe(
            columns=columns,
            data=data
        )
        
        df = df.fillna(value=np.nan)
        return df
        
    def get_report(
        self,
        detail:dict,
        start_date:datetime,
        end_date:datetime,
        scale:str='down_scale_15'
        )->Union[pd.DataFrame,None]:
        """
        Return raw_report with change column names
        """

        df = self.get_raw_report(
            detail=detail,
            start_date=start_date,
            end_date=end_date,
            scale=scale
        )

        return self.parse_response(
            df=df,
            patterns = detail['patterns']
            )

    def parse_info_sensors_to_df(
        self,
        payload:dict, # we use QantumReports.set_payload_report() method
        )->pd.DataFrame:
        info_sensores = self.get_info_sensors(payload=payload)
        data = [(id,info_sensores[id]['name']) for id in info_sensores.keys()]
        df_info = pd.DataFrame(columns = ['id sensor','Nombre'],data=data)
        return df_info