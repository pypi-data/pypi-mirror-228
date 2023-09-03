from typing import Union
from .auth import GpmAuth
from .utils import GpmUtils
import pandas as pd
import logging
from datetime import datetime
from functools import reduce

class GpmReports(
    GpmAuth,
    GpmUtils
    ):

    def __init__(
        self, 
        user: str, 
        pssw: str, 
        ssl_path: Union[str,None] = None
        ) -> None:

        super().__init__(user, pssw, ssl_path)
        #--- Paths ---#
        self.REPORT_PATH = '/api/analysis/table'
        #--- Init login ---#
        self.login_status = self.login()

    def set_url_report(
        self,
        start_date:datetime,
        end_date:datetime,
        id_planta:int,
        id_report:int,
        timezone:str='-04:00'
        )-> str:

        logging.debug("(fnc) GpmClient.parse_url_report() ")

        start_timestamp = start_date.strftime('%Y-%m-%d')+'T00:00:00'+ timezone
        finish_timestamp = end_date.strftime('%Y-%m-%d')+'T23:59:59'+ timezone
        ENDPOINT_PATH = '/'+str(id_planta)+'/'+str(id_report)+'/'+start_timestamp+'/'+finish_timestamp
        url = self.BASE_URL + self.REPORT_PATH + ENDPOINT_PATH

        return url

    def get_report(
        self,
        start_date:datetime,
        end_date:datetime,
        id_planta:int,
        id_report:int,
        report_name:str
        )->Union [pd.DataFrame , None]:
        """
        Get specific refort from ID 
        """
        # logging.info(f">> Get report {planta} {report_name}")

        URL = self.set_url_report(
            start_date=start_date,
            end_date=end_date,
            id_planta=id_planta,
            id_report=id_report
            )
        self.session.headers['content-type'] = None

        response = self.GET(
            url = URL,
            header= self.session.headers
        )

        if response.status_code == 200:
            try:
                return self.parse_json(
                    data=response.json()
                    )
                
            except Exception as e:
                logging.warning(f"ERROR when try parse json from response as : {e}")

        logging.warning(f"return None when get report:  {report_name}")
        
        return None
    
    def get_multiple_reports(
        self,
        start_date:datetime,
        end_date:datetime,
        id_planta:int,
        list_id_reports:list,
        reports_name:str,
        column_on_merge:str='Fecha',
        mode_of_merge:str ='outer'
        ):
        # try to get all DF (return None if not success)
        list_df = [
            self.get_report(
                start_date = start_date,
                end_date = end_date,
                id_planta = id_planta,
                id_report= id_report,
                report_name=reports_name
            ) for id_report in list_id_reports
        ]

        # filter None values
        list_df = list(filter(lambda x: x is not None, list_df))

        # Merge all DF
        return reduce(
            lambda left,right: pd.merge(
                left, 
                right, 
                on= column_on_merge, 
                how=mode_of_merge
                ), 
            list_df)