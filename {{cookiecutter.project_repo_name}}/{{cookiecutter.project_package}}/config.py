import json
import os

import yaml


class Config:
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state

    def get_service_account_info(self) -> dict:
        sa_info = os.getenv("SERVICE_ACCOUNT_INFO")
        if sa_info:
            sa_info = json.loads(sa_info)
        else:
            with open(self.service_account_file) as rf:
                sa_info = json.load(rf)
        return sa_info

    @staticmethod
    def load(path: str) -> 'Config':
        with open(path) as rf:
            Config.__shared_state = yaml.load(rf)
        return Config()
