import os
from collections import UserDict
from typing import Optional

from yarl import URL


class ServiceParameters(UserDict):
    def __init__(self):
        super().__init__()

    @property
    def region(self) -> str:
        return self.get_key("AWS_REGION")

    @property
    def dynamodb_url(self) -> Optional[URL]:
        dynamodb_url = self.get_key("DYNAMODB_URL")
        return URL(dynamodb_url) if dynamodb_url else None

    @property
    def service_data_table_name(self) -> str:
        return self.get_key("DATA_TABLE", "tdc-dev-data")

    def get_key(self, key: str, default_value: str = "") -> str:
        value = self.__find_from_environment(key)
        if value is not None:
            return value
        return default_value

    @staticmethod
    def __find_from_environment(key: str):
        return os.environ.get(key)


parameters = ServiceParameters()
