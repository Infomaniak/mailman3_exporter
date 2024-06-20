import requests
import logging
from typing import Any
from src.settings import Settings


class Api:
    def __init__(self, settings: Settings):
        self.settings = settings
        url = self.mailman_url('/')
        logging.info(f"Querying Mailman at URL: <{url}>")

    def mailman_url(self, uri: str = "") -> str:
        return f"{self.settings.mailman_address}/{self.settings.mailman_api_version}{uri}"

    def usercount(self) -> tuple[int, Any]:
        response = {'status_code': 0}
        try:
            usrs = {}
            url = self.mailman_url("/users?count=1&page=1")
            response = requests.get(url, auth=(self.settings.mailman_user, self.settings.mailman_password))
            if 200 <= response.status_code < 220:
                usrs = response.json()
        except Exception as e:
            logging.error(f"usercount(exception): {e}")
            return 500, {}

        logging.debug("usercount: url %s" % response.request.url)
        logging.debug("usercount: content %s" % response.content[:160])
        return response.status_code, usrs

    def versions(self) -> tuple[int, Any]:
        response = {'status_code': 0, 'request': ''}
        try:
            url = self.mailman_url("/system/versions")
            response = requests.get(url, auth=(self.settings.mailman_user, self.settings.mailman_password))
        except Exception as e:
            logging.error(f"versions(exception): {e}")
            return 500, {}

        logging.debug("versions: url %s" % response.request.url)
        logging.debug("versions: content %s" % response.content[:160])
        return response.status_code, response

    def domains(self) -> tuple[int, Any]:
        response = {'status_code': 0}
        domains = {}
        try:
            url = self.mailman_url("/domains")
            response = requests.get(url, auth=(self.settings.mailman_user, self.settings.mailman_password))
            if 200 <= response.status_code < 220:
                domains = response.json()
        except Exception as e:
            logging.error(f"domains(exception): {e}")
            return 500, {}

        logging.debug("domains: url %s" % response.request.url)
        logging.debug("domains: content %s" % response.content[:160])
        return response.status_code, domains

    def lists(self) -> tuple[int, Any]:
        response = {'status_code': 0}
        lists = {}
        try:
            url = self.mailman_url("/lists")
            response = requests.get(url, auth=(self.settings.mailman_user, self.settings.mailman_password))
            if 200 <= response.status_code < 220:
                lists = response.json()
        except Exception as e:
            logging.error(f"lists(exception): {e}")
            return 500, {}

        logging.debug("lists: url %s" % response.request.url)
        logging.debug("lists: content %s" % response.content[:160])
        return response.status_code, lists

    def queues(self) -> tuple[int, Any]:
        response = {'status_code': 0}
        queues = {}
        try:
            url = self.mailman_url("/queues")
            response = requests.get(url, auth=(self.settings.mailman_user, self.settings.mailman_password))
            if 200 <= response.status_code < 220:
                queues = response.json()
        except Exception as e:
            logging.error(f"queues(exception): {e}")
            return 500, {}

        logging.debug("queues: url %s" % response.request.url)
        logging.debug("queues: content %s" % response.content[:120])
        return response.status_code, queues
