from datetime import datetime
from typing import Union
import logging
import re
import pandas as pd

from ..common import BaseClient

class GpmClient(BaseClient):
    def __init__(
        self,
        user:str,
        pssw:str,
        ssl_path:Union[str,None] = None
        ) -> None:
        super().__init__(ssl_path=ssl_path)

        logging.info('>> Init GPM both...')
        #---URLs & paths---#
        self.LOGIN_URL = 'https://gpmportal.greenpowermonitor.com/application/login'
        self.LOGIN_URL_CHECK = 'https://gpmportal.greenpowermonitor.com/application/login_check'

        #---credentials---#
        self.USER = user
        self.PASSWORD = pssw

    def __get_csrf_token(
        self,
        text:str
        )->str:

        logging.debug('(fnc) GpmClient.__get_csrf_token()')
        pattern = r'(<input\stype="hidden"\s(name="_csrf_token")\svalue="(.*)"\s/>)'
        result = re.search(pattern,text)
        raw_data = text[result.start():result.end()]
        return raw_data.split('"')[-2]

    def login(
        self,
        )->bool:
        
        logging.info('>> Sign in GPM')
        
        response = self.GET(
            url = self.LOGIN_URL,
            header = self.headers
            )
        
        if response.status_code == 200:

            self.headers['cookie'] = '; '.join([x.name + '=' + x.value for x in response.cookies])
            self.headers['content-type'] = 'application/x-www-form-urlencoded'

            payload = {
                '_csrf_token':self.__get_csrf_token(text = response.text),
                'redirectFailure':'',
                '_username': self.USER,
                '_password': self.PASSWORD,
                'submit_show':'Entrar',
                '_submit':'Entrar'
            }

            response = self.POST(
                url = self.LOGIN_URL_CHECK, 
                header = self.headers,
                payload = payload, 
                )

            logging.debug('Get cookies')
            self.headers['cookie'] = '; '.join([x.name + '=' + x.value for x in response.history[0].cookies])
            logging.debug(f" >> cookie:{self.headers['cookie']}")
            
            
            return True
        else:
            logging.error(f"Error login - response status_code: {response.status_code}")
            return False

    def parse_url_report(
        self,
        start_date:datetime,
        end_date:datetime,
        id_planta:int,
        id_report:int,
        )-> str:

        logging.debug("(fnc) GpmClient.parse_url_report() ")
        start_timestamp = start_date.strftime('%Y-%m-%d')+'T00:00:00-04:00'
        finish_timestamp = end_date.strftime('%Y-%m-%d')+'T23:59:59-04:00'
        url='https://gpmportal.greenpowermonitor.com/application/api/analysis/table/'+str(id_planta)+'/'+str(id_report)+'/'+start_timestamp+'/'+finish_timestamp
        
        return url

    def get_report(
        self,
        url_report:str,
        planta:str,
        report_name:str
        )->Union [pd.DataFrame , None]:
        
        logging.info(f">> Get report {planta} {report_name}")

        response = self.GET(
            url = url_report,
            header= self.headers
        )

        if response.status_code == 200:
            try:
                return self.parse_json(
                    data=response.json()
                    )
                
            except Exception as e:
                logging.warning(f"ERROR when try parse json from response as : {e}")

        logging.warning(f"return None when get report: {planta} {report_name}")
        
        return None
    
    """ UTILS """
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
     
     
if __name__ =='__main__':
    print('hola')
    pass 