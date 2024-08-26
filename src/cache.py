import time
import logging
from src.api import Api
from typing import Any
from src.config import Config


class Cache:
    def __init__(self, api: Api, config: Config):
        self.api = api
        self.config = config
        self.last_data_refresh_time = 0
        self.refresh_data = True

        self._domains_status = 0
        self._domains = []
        self._lists_status = 0
        self._lists = []

    def refresh_time(self):
        if not self.config.enable_caching:
            return
        now = time.monotonic()
        elapsed_time = now - self.last_data_refresh_time
        if elapsed_time > self.config.cache_duration_in_seconds:
            logging.debug("refresh cache data")
            self.refresh_data = True
            self.last_data_refresh_time = now
        else:
            self.refresh_data = False

    def domains(self) -> tuple[int, Any]:
        if self.refresh_data:
            self._domains_status, self._domains = self.api.domains()
        return self._domains_status, self._domains

    def lists(self) -> tuple[int, Any]:
        if self.refresh_data:
            self._lists_status, self._lists = self.api.lists()
        return self._lists_status, self._lists
