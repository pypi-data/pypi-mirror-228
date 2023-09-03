import logging
import requests
from typing import Union

class BaseClient():
    """
    Base client to execute HTTP methods -> POST & GET
    """
    def __init__(
        self,
        ssl_path:Union[str,None] = None
        ) -> None:

        self.SSL_PATH = ssl_path

        #---Session---#
        logging.debug('>> Init session')
        self.session = requests.Session()
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
            }
    
    def GET(
        self, #Por aquí pasó el Manuel
        url:str,
        header:dict,
        params:Union[dict,None]=None
        )-> requests.Response:

        logging.debug(f"(fnc) BaseClient.GET(url = {url} )")

        try:
            if self.SSL_PATH != None:
                response = self.session.get(
                    url = url,
                    headers = header,
                    params = params,
                    verify = self.SSL_PATH,
                    )
            
            else:
                response = self.session.get(
                    url = url,
                    headers = header,
                    params = params,
                    )
            
            if response.status_code != 200:
                logging.warning(f"Empty response when we try GET {url} \nResponse status code: {response.status_code}")
    
            return response #Por aquí también
    
        except Exception as e:
            logging.error(f"ERROR when try execute GET method: {e}")
            return requests.Response

    def POST(
        self,
        url:str,
        header:dict,
        payload:dict,
        ) -> requests.Response:

        logging.debug(f"(fnc) BaseClient.POST(url = {url} )")

        try: 
            if self.SSL_PATH != None:
                response = self.session.post(
                    url = url,
                    headers = header,
                    data = payload,
                    verify=self.SSL_PATH,
                    )
            
            else:
                response = self.session.post(
                    url = url,
                    headers = header,
                    data = payload,
                    )
            
            if response.status_code != 200:
                logging.warning(f"Empty response when we try POST {url} \nResponse status code: {response.status_code}")
    
            return response

        except Exception as e:
            logging.error(f"ERROR when try execute POST method: {e}")
            return requests.Response
    
    def update_cookies(
        self,
        response_cookies
        ) -> None:
        logging.debug('Update session cookies')
        self.session.headers['cookie'] = '; '.join([x.name + '=' + x.value for x in response_cookies])

if __name__ == '__main__':
    
    pass
    