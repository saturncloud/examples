import mixpanel
import os
from urllib.parse import urlparse

import os

try:
    token = "48492526e4cdc4c41a809e81ab82bcff"
    mp = mixpanel.Mixpanel(token)
except Exception as e:
    pass


def progress(name:str, domain: str = None, username: str = None, url: str = None):
    try:
        _progress(name, domain, username, url)
    except Exception as e:
        pass
    
    
def _progress(name:str, domain: str = None, username: str = None, url: str = None):    
    orgname = None
    if domain is None:
        domain = os.getenv('SATURN_JUPYTER_BASE_DOMAIN')
        split = os.getenv("SATURN_JUPYTER_BASE_DOMAIN").rsplit('.', 3)
        if len(split) == 4:
            orgname = split[1]
    if username is None:
        username = os.getenv('SATURN_USERNAME')
    if url is None:
        url = os.getenv('SATURN_JUPYTER_BASE_URL')
    if username is None or domain is None or url is None:
        return
    mp.track(
        f"{orgname}:{username}",
        name,
        properties={
            "$current_url": url,
            "username": username,
            "orgname": orgname
        },
    )
