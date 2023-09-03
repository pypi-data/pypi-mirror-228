from ..common import BaseClient
from typing import Union
import logging
import re

class GpmAuth(BaseClient):
    def __init__(
        self,
        user:str,
        pssw:str,
        ssl_path:Union[str,None] = None
        ) -> None:
        super().__init__(ssl_path=ssl_path)

        logging.info('>> Init GPM both...')
        #---URLs & paths---#
        self.BASE_URL = 'https://gpmportal.greenpowermonitor.com/application'
        self.LOGIN_PAGE_PATH = '/login'
        self.LOGIN_CHECK_PATH = '/login_check'

        #---credentials---#
        self.USER = user
        self.PASSWORD = pssw

    def __get_csrf_token(
        self,
        text:str
        )->str:
        """
        Get CSRF token with apply regex function
        """
        logging.debug('(fnc) GpmClient.__get_csrf_token()')
        pattern = r'(<input\stype="hidden"\s(name="_csrf_token")\svalue="(.*)"\s/>)'
        result = re.search(pattern,text)
        raw_data = text[result.start():result.end()]
        return raw_data.split('"')[-2]

    def get_login_page(
        self
        )->tuple:
        """
        Get text and response.cookies form Login page
        """
        URL = self.BASE_URL + self.LOGIN_PAGE_PATH

        response = self.GET(
            url = URL,
            header = self.headers
            )

        if response.status_code != 200:
            logging.error(f"Error get login page - response status_code: {response.status_code}")
            return None,None
        
        token = self.__get_csrf_token(text = response.text)
        cookies = response.cookies
        return token,cookies
        
    def send_credentials(
        self,
        payload:dict
        ):
        """
        Send form with credentials of GPM user
        """
        URL = self.BASE_URL + self.LOGIN_CHECK_PATH

        response = self.POST(
            url = URL, 
            header = self.session.headers,
            payload = payload, 
            )
        
        if response.status_code/100 >= 4:
            # creo que se redirecciona el ultimo response asi que mientras sea code 200.. o 300.. esta bien 
            return False

        self.update_cookies(response_cookies=response.history[0].cookies)
        return True

    def login(
        self,
        )->bool:
        """
        Pipeline with all steps of login
        """
        logging.info('>> Login GPM')
        
        token,cookies = self.get_login_page()

        if token == None:
            return False
        

        self.update_cookies(response_cookies=cookies)
        self.session.headers['content-type'] = 'application/x-www-form-urlencoded'

        payload = {
            '_csrf_token':token,
            'redirectFailure':'',
            '_username': self.USER,
            '_password': self.PASSWORD,
            'submit_show':'Entrar',
            '_submit':'Entrar'
        }

        login_status = self.send_credentials(
            payload=payload
        )

        return login_status
        