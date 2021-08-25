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

    @staticmethod
    def get_key(key: str, default_value: str = "") -> str:
        return os.environ.get(key, default_value)


parameters = ServiceParameters()
