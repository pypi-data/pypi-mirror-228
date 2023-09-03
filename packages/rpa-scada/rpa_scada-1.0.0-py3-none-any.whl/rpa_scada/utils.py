import os
from os.path import join, dirname
from dotenv import load_dotenv
import logging

def get_credentials(
    platform:str,
    env_file:str = 'scada.env'
    )->dict:
    """
    DESCRIPTION
        function to load and read credentials from .env file
      
    INPUT
    * platform (str) -> options ->  gpm | qantum

    RETURN: dict of credentials
    * sql_server -> keys = [ 'HOST_DB' , 'NAME_DB' , 'USER_DB' , 'PASSWORD_DB' ] 
    * gpm | qantum -> keys = [ 'USER' , 'PASSWORD' ]

    """
    logging.debug(f"(fnc) src.get_credentials(platform={platform})")

    dotenv_path = join(dirname(__file__), env_file)
    load_dotenv(dotenv_path)

    credentials = {}


    if platform == 'gpm':
        credentials={
            'USER' : os.environ.get("USER_GPM"),
            'PASSWORD' : os.environ.get("PSSW_GPM")
        }
    
    elif platform == 'qantum':
        credentials={
            'USER' : os.environ.get("USER_QANTUM"),
            'PASSWORD' : os.environ.get("PSSW_QANTUM")
        }

    return credentials

def init_logging(
    mode:str='info'
    ):

    MODE = logging.INFO if mode=='info' else logging.DEBUG

    logging.basicConfig(
        level=MODE,
        format="%(asctime)s %(levelname)s:%(name)s - %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S',
        )
