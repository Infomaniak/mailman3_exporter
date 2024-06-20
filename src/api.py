from  requests import get, Response
import logging
from typing import Any
from src.settings import Settings

DEFAULT_RESPONSE = {'status_code': 0}


class Api:
    def __init__(self, settings: Settings):
        self.settings = settings
        url = self.mailman_url('/')
        logging.info(f"Querying Mailman at URL: <{url}>")

    def mailman_url(self, uri: str = "") -> str:
        return f"{self.settings.mailman_address}/{self.settings.mailman_api_version}{uri}"

    def make_request(self, name: str, endpoint: str) -> tuple[int, Any]:
        url = self.mailman_url(endpoint)
        try:
            response = get(url, auth=(self.settings.mailman_user, self.settings.mailman_password))
            if 200 <= response.status_code < 220:
                return response.status_code, response.json()
            else:
                logging.debug(f"{name}: url {url}")
                logging.debug(f"{name}: content {response.content[:160]}")
                return response.status_code, {}
        except Exception as e:
            logging.error(f"{name}(exception): {e}")
            return 500, {}

    def usercount(self) -> tuple[int, Any]:
        return self.make_request('usercount', '/users?count=1&page=1')

    def versions(self) -> tuple[int, Any]:
        return self.make_request('versions', '/system/versions')

    def domains(self) -> tuple[int, Any]:
        return self.make_request('domains', '/domains')

    def lists(self) -> tuple[int, Any]:
        return self.make_request('lists', '/lists')

    def queues(self) -> tuple[int, Any]:
        return self.make_request('queues', '/queues')
