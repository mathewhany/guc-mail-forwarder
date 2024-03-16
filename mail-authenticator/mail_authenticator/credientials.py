from dataclasses import dataclass
import os
from typing import Protocol


@dataclass
class Credientials:
    username: str
    password: str
    
    
class CredentialsLoader(Protocol):
    def load(self, username: str) -> Credientials:
        pass


class EnvVarCredentialsLoader:
    def load(self, username: str) -> Credientials:
        username = os.getenv('GUC_USERNAME')
        password = os.getenv('GUC_PASSWORD')
        
        if username is None or password is None:
            raise ValueError('Username or password not found. Please set MAIL_POLLER_USERNAME and MAIL_POLLER_PASSWORD environment variables.')
        
        return Credientials(username, password)
