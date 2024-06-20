import time
from prometheus_client.core import GaugeMetricFamily
import logging


class metric_processing_time:
    def __init__(self, name: str, processing_time: GaugeMetricFamily):
        self.start = None
        self.name = name
        self.processing_time = processing_time

    def __enter__(self):
        self.start = time.process_time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = (time.process_time() - self.start) * 1000
        logging.debug('Processing %s took %s miliseconds' % (self.name, elapsed))
        self.processing_time.add_metric([self.name], elapsed)