import hashlib
import hmac
import base64
from time import time
from random import randint
from typing import Union


__author__ = '139928764+p4irin@users.noreply.github.com'
__version__ = '0.1.1'


def generate(
        username: Union[str, None]=None, shared_secret: str='',
        ttl: int=86400  # One day
    ) -> dict:

    """Generate time limited, ephemeral, long term credentials
    
    , to authenticate usage of a coturn server.
    """

    expiration_timestamp = int(time()) + ttl

    username = username if username else f'{randint(10000, 99999)}'
    if not shared_secret:
        raise Exception(
            'A secret you share with a coturn server is mandatory!'
        )
    coturn_username = f'{expiration_timestamp}:{username}'

    dig = hmac.new(
        shared_secret.encode(), coturn_username.encode(),
        hashlib.sha1
    ).digest()
    coturn_password = base64.b64encode(dig).decode()

    return {
        "coturn_username": coturn_username,
        "coturn_password": coturn_password
    }
