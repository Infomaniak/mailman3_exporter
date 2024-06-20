import time
import logging
from src.api import Api
from typing import Any

DEFAULT_CACHE_DURATION_IN_SECONDS = 30


class Cache:
    def __init__(self, api: Api, cache_duration_in_seconds=DEFAULT_CACHE_DURATION_IN_SECONDS):
        self.api = api
        self.cache_duration_in_seconds = cache_duration_in_seconds
        self.last_data_refresh_time = 0
        self.refresh_data = True

        self._domains_status = 0
        self._domains = []
        self._lists_status = 0
        self._lists = []

    def refresh_time(self):
        now = time.monotonic()
        elapsed_time = now - self.last_data_refresh_time
        if elapsed_time > self.cache_duration_in_seconds:
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
