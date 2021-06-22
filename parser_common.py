""" Module with common code for parsers. """

import requests


def read_file(name: str) -> str:
    """Read data from file."""
    with open(name) as file:
        return file.read()


def download_data_from_site(data_url: str) -> str:
    """Download data from site with specified URL"""
    try:
        result = requests.get(data_url)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError):
        raise ConnectionError("Cannot download data from site")


def write_to_file(name: str, content: str) -> None:
    """Write content to file."""
    with open(name, "w") as pretty_file:
        pretty_file.write(content)
