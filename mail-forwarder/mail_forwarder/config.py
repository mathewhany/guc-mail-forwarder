from dataclasses import dataclass
import os
from typing import Protocol

@dataclass
class Config:
    authenticator_url: str
    redis_host: str
    redis_port: int
    kafka_bootstrap_servers: str
    username: str
    forward_to_mail: str
    
class ConfigLoader(Protocol):
    def load_config(self) -> None:
        pass
    
class EnvVarsConfigLoader:
    def load_config(self) -> Config:        
        authenticator_url = os.getenv('AUTHENTICATOR_URL')
        redis_host = os.getenv('REDIS_HOST')
        redis_port = os.getenv('REDIS_PORT')
        kafka_bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
        forward_to_mail = os.getenv('FORWARD_TO_MAIL')
        guc_username = os.getenv('GUC_USERNAME')

        return Config(
            authenticator_url=authenticator_url,
            redis_host=redis_host,
            redis_port=redis_port,
            kafka_bootstrap_servers=kafka_bootstrap_servers,
            forward_to_mail=forward_to_mail,
            username=guc_username
        )
