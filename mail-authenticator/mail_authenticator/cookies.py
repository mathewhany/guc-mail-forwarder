import json
import os
from typing import Protocol
import requests


class CookieLoader(Protocol):
    def load(self, username: str) -> requests.cookies.RequestsCookieJar:
        pass
     
     
class CookiesSaver(Protocol):
    def save(self, username: str, cookies: requests.cookies.RequestsCookieJar):
        pass


class JsonCookieLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        
    def load(self, username: str) -> requests.cookies.RequestsCookieJar:
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                return requests.cookies.cookiejar_from_dict(json.load(file))
        else:
            return None


class JsonCookieSaver:
    def __init__(self, file_path: str):
        self.file_path = file_path
        
    def save(self, username: str, cookies: requests.cookies.RequestsCookieJar):
        with open(self.file_path, 'w') as file:
            json.dump(requests.utils.dict_from_cookiejar(cookies), file)
    