#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Prometheus mailman3 exporter using rest api's.
    Created by rivimey.
"""
import logging
import sys
import signal
import time
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY
from src.settings import Settings
from src.collector import Collector
from src.api import Api


def index() -> str:
    return """
<html><head><title>Mailman3 Prometheus Exporter</title></head>
<body>
<h1>Mailman3 Prometheus Exporter</h1>
<p>Prometheus metrics bridge for the Mailman3 REST API</p>
<p>Visit the metrics page at: <a href="/metrics">/metrics</a>.</p>
</body>
"""


def signal_handler(_sig: int, _frame: None) -> None:
    shutdown(1)


def shutdown(code: int) -> None:
    logging.info('Shutting down')
    sys.exit(code)


def main() -> None:
    signal.signal(signal.SIGTERM, signal_handler)

    settings = Settings()
    api = Api(settings)

    logging.info('Starting server...')
    start_http_server(addr=settings.hostname, port=settings.port, registry=REGISTRY)
    logging.info('Server started on port %s', settings.port)

    REGISTRY.register(Collector(api))
    while True:
        time.sleep(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
