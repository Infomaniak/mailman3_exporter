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
from src.collectors.platform_collector import PlatformCollector
from src.collectors.gc_collector import GCCollector
from src.config import Config, DEFAULT_WAIT_FOR_MAILMAN_SLEEP_INTERVAL_IN_SECONDS
from src.collectors.mailman3_collector import Mailman3Collector
from src.api import Api
from time import sleep


def signal_handler(_sig: int, _frame: None) -> None:
    shutdown(1)


def shutdown(code: int) -> None:
    logging.info('Shutting down')
    sys.exit(code)


def wait_for_mailman(api: Api, interval_in_seconds: float = DEFAULT_WAIT_FOR_MAILMAN_SLEEP_INTERVAL_IN_SECONDS) -> None:
    while True:
        status, resp = api.versions()
        if 200 <= status < 220:
            return
        else:
            logging.info(f"Mailman connection failed, sleeping... (status: {status})")
            sleep(interval_in_seconds)


def main() -> None:
    signal.signal(signal.SIGTERM, signal_handler)

    config = Config()
    api = Api(config)

    wait_for_mailman(api)

    logging.info('Starting server...')
    registry = CollectorRegistry()

    if config.enable_gc_metrics:
        GCCollector(namespace=config.namespace, registry=registry)
    if config.enable_platform_metrics:
        PlatformCollector(namespace=config.namespace, registry=registry)
    if config.enable_process_metrics:
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
