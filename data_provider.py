import requests
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class DataProvider(ABC):
    """ Abstract class to form the structure of all data providers and provide basic functionality."""

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def parse_data(self, data: Any):
        pass

    @staticmethod
    @abstractmethod
    def convert_date(text: str) -> datetime:
        """ Change format for date field."""
        pass

    @staticmethod
    def read_file(name: str) -> str:
        """Read data from file."""
        with open(name) as file:
            return file.read()

    @staticmethod
    def download_data_from_site(data_url: str) -> str:
        """Download data from site with specified URL"""
        try:
            result = requests.get(data_url)
            result.raise_for_status()
            return result.text
        except (requests.RequestException, ValueError):
            raise ConnectionError("Cannot download data from site")

    @staticmethod
    def write_to_file(name: str, content: str) -> None:
        """Write content to file."""
        with open(name, "w") as pretty_file:
            pretty_file.write(content)
