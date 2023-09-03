import logging
from ..common import BaseClient
from typing import Union
import json 

class QantumAuth(BaseClient):
    def __init__(
        self,
        user:str,
        pssw:str,
        ssl_path: Union[str, None] = None
        ) -> None:

        super().__init__(ssl_path)

        logging.info('>> Init QANTUM bot...')

        #---URLs & paths---#
        self.BASE_URL = 'https://qantum.qosenergy.com'
        self.LOGIN_PAGE_PATH = '/app/auth/' # GET
        self.LOGIN_PATH = '/api/auth/user/login' # POST
        self.URL_VERIFY_PATH = '/api/auth/session/verify' # GET
        self.REFRESH_PATH = '/api/auth/session/refresh' # POST 
        #---credentials---#
        self.USER = user
        self.PASSWORD = pssw

    def get_login_page(
        self
        ) -> None:
        """
        DESCRIPTION:
            Method to het login page (the execute is not necesary to login)
        
        INPUT PARAMETERS:
            None
        
        RETURN PARAMETERS:
            None
        """
        URL = self.BASE_URL + self.LOGIN_PAGE_PATH
        response = self.GET(
            url = URL,
            header = self.headers,
            )
        
        logging.debug(response.status_code)
        
    def login(
        self
        )->bool:
        """
        DESCRIPTION
            Method to get cookies, that we use to authentication on future requests

        INPUT PARAMETERS: 
            None

        RETURN PARAMETERS:
            BOOL:
            * True if response code of login is 200
            * False on other case 
        """

        URL = self.BASE_URL + self.LOGIN_PATH
        payload = {
            "email": self.USER,
            "password": self.PASSWORD,
            "remember": False
        }
        header_form = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'Accept':'application/json, text/plain, */*',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'es-ES,es;q=0.9',
            'Content-Type':'application/json',
            'Origin':self.BASE_URL,
            'Referer':self.BASE_URL + self.LOGIN_PAGE_PATH,
            'Sec-Ch-Ua':'"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'Sec-Ch-Ua-Mobile':'?0',
            'Sec-Ch-Ua-Platform':'"Windows"',
            'Sec-Fetch-Dest':'empty',
            'Sec-Fetch-Mode':'cors',
            'Sec-Fetch-Site':'same-origin'
            }
        self.session.headers.update(header_form)
        logging.debug('execute POST request')
        response = self.POST(
            url = URL, 
            payload = json.dumps(payload,separators=(',',':')).encode('utf-8'), 
            header = header_form
            )
        
        if response.status_code == 200:
            logging.info(">> Login status check")
            # update headers of session
            # self.session.headers['cookie'] = '; '.join([x.name + '=' + x.value for x in response.cookies])
            self.update_cookies(response_cookies = response.cookies)
            logging.debug(f"Cookie: {self.session.headers['cookie']}")
            return True
        
        logging.warning(f"Error when sign in \n response status code: {response.status_code}")
        return False
    
    def close(
        self
        )->None:
        self.session.close()
    
    def update_cookies(
        self,
        response_cookies
        ) -> None:
        self.session.headers['cookie'] = '; '.join([x.name + '=' + x.value for x in response_cookies])
        

if __name__ == '__main__':

    pass