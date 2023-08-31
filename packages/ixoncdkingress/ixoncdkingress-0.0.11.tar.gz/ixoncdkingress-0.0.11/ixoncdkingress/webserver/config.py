"""
Contains the configuration for the ixoncdkingress webserver
"""
import enum
import json
import sys

from functools import reduce
from logging import Formatter, Logger, StreamHandler, getLogger
from typing import List, Mapping, Optional, Union, Dict, Any, Tuple

from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.serialization import load_pem_public_key

class InvalidConfigException(Exception):
    """
    Exception for invalid values in the config
    """

class WsgiProvider(enum.Enum):
    """
    Provider to use to turn a WSGI application into a (HTTP) server
    """
    WSGIREF = 'wsgiref'
    BJOERN = 'bjoern'
    WAITRESS = 'waitress'
    GUNICORN = 'gunicorn'
    CHERRYPY = 'cherrypy'
    MEINHELD = 'meinheld'

class Config:
    """
    Configuration for the webserver
    """
    @classmethod
    def from_environ(cls, environ: Mapping[str, str]) -> 'Config':
        """
        Parses an environment disctionary and generates a config based on it
        """

        res = cls()

        res.production_mode = load_bool_from_environment(environ, 'PRODUCTION_MODE', False)

        res.http_server_bind = environ.get('HTTP_SERVER_BIND', '127.0.0.1')
        res.http_server_port = int(environ.get('HTTP_SERVER_PORT', '8020'))
        res.document_db_port = int(environ.get('DOCUMENT_DB_PORT', '27017'))

        res.wsgi_provider = WsgiProvider(environ.get('WSGI_PROVIDER', 'wsgiref'))

        res.logger_log_level = environ.get('LOGGER_LOG_LEVEL', 'INFO')
        res.logger_format = environ.get(
            'LOGGER_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        res.version = load_str_file(environ.get('VERSION_PATH'), 'dev')

        res.cbc_path = environ.get('CBC_PATH', '/user_scripts')

        res.api_client_base_url = environ.get('API_CLIENT_BASE_URL', 'https://api.ayayot.com/')

        cbc_signature_public_keys = environ.get('CBC_SIGNATURE_PUBLIC_KEYS', '')
        res.signature_public_keys = (cbc_signature_public_keys.split(',')
                                     if cbc_signature_public_keys != '' else [])

        return res

    production_mode: bool

    document_db_port: int

    http_server_bind: str
    http_server_port: int
    wsgi_provider: WsgiProvider

    logger_log_level: Union[int, str]
    logger_format: str

    version: str
    cbc_path: str
    api_client_base_url: str

    signature_public_keys: List[str]

    _logger: Optional[Logger]
    _signature_public_keys: Optional[List[ed25519.Ed25519PublicKey]]

    def __init__(self) -> None:
        self._logger = None
        self._signature_public_keys = None

    def get_logger(self) -> Logger:
        """
        Returns a logger
        """
        if self._logger is None:
            logger = getLogger('ixoncdkingress')
            logger.setLevel(self.logger_log_level)

            handler = StreamHandler(sys.stdout)
            handler.setFormatter(Formatter(self.logger_format))
            logger.addHandler(handler)

            self._logger = logger

        return self._logger

    def get_signature_public_keys(self) -> List[ed25519.Ed25519PublicKey]:
        """
        Returns a cached instance of signature public keys
        """
        if self._signature_public_keys is None:
            keys: List[ed25519.Ed25519PublicKey] = []

            for index, pem in enumerate(self.signature_public_keys):
                key = load_pem_public_key(pem.encode('ASCII'), None)
                assert isinstance(key, ed25519.Ed25519PublicKey), \
                    f'signature_public_key {index + 1} is not a valid Ed25519 private key'
                keys.append(key)

            self._signature_public_keys = keys
        return self._signature_public_keys

def load_str_file(
        file_path: Optional[str], default: str
    ) -> str:
    """
    Loads a string from a file, returns default if no path is given
    """
    if not file_path:
        return default

    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            string = file.read().rstrip()
            if not string:
                return default
        return string
    except IOError:
        return default

def to_str_value(acc: Dict[str, str], val: Tuple[str, Any]) -> Dict[str, str]:
    """
    Reducer function to convert a dict entry value to string.
    """
    return acc | { val[0]: str(val[1])}

def load_bool_from_environment(environ: Mapping[str, str], key: str, default: bool) -> bool:
    """
    Loads a boolean value from the environment
    """
    val_str = environ.get(key, default)
    if val_str is default or val_str == '':
        return default

    if val_str not in ('False', 'True'):
        raise InvalidConfigException(f'Invalid boolean value: {val_str}')

    return 'True' == val_str

def load_json_file(
        file_path: Optional[str], default: Dict[str, str]
    ) -> Dict[str, str]:
    """
    Loads a Dict from a JSON file, converting all numeric values to string. Returns default if no
    path is given, file_path does not exist, or file_path does not contain a JSON file.
    """
    if not file_path:
        return default

    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            result = json.load(file, parse_int=str, parse_float=str)
            if not result:
                return default

        values = result['values']

        return reduce(to_str_value, values.items(), {})
    except IOError:
        return default
