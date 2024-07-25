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
from prometheus_client import start_http_server, CollectorRegistry, ProcessCollector
from src.platform_collector import PlatformCollector
from src.gc_collector import GCCollector
from src.config import Config
from src.mailman3_collector import Mailman3Collector
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

    config = Config()
    api = Api(config)

    logging.info('Starting server...')
    registry = CollectorRegistry()

    GCCollector(namespace=config.namespace, registry=registry)
    PlatformCollector(namespace=config.namespace, registry=registry)
    ProcessCollector(namespace=config.namespace, registry=registry)
    Mailman3Collector(api=api, config=config, registry=registry)

    start_http_server(addr=config.hostname, port=config.port, registry=registry)
    logging.info(f"Server started on port {config.port}")

    while True:
        time.sleep(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
