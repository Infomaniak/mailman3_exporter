from argparse import ArgumentParser, Namespace
import logging
import re

ENABLED_TEXT = 'true'
DISABLED_TEXT = 'false'
BOOLEAN_CHOICES = [ENABLED_TEXT, DISABLED_TEXT]

DEFAULT_MAILMAN_API_VERSION = "3.1"

DEFAULT_LOG_LEVEL = 'info'

DEFAULT_LOG_CONFIG = DISABLED_TEXT

DEFAULT_HOSTNAME = 'localhost'
DEFAULT_PORT = 9934

DEFAULT_MAILMAN_ADDRESS = 'http://mailman-core:8001'

DEFAULT_MAILMAN_USERNAME = 'restadmin'
DEFAULT_MAILMAN_PASSWORD = 'restpass'

DEFAULT_NAMESPACE = ''

DEFAULT_CACHE_ENABLED = ENABLED_TEXT
DEFAULT_CACHE_DURATION_IN_SECONDS = 30

DEFAULT_ENABLE_GC_METRICS = ENABLED_TEXT
DEFAULT_ENABLE_PLATFORM_METRICS = ENABLED_TEXT
DEFAULT_ENABLE_PROCESS_METRICS = ENABLED_TEXT
DEFAULT_ENABLE_DOMAINS_METRICS = ENABLED_TEXT
DEFAULT_ENABLE_LISTS_METRICS = ENABLED_TEXT
DEFAULT_ENABLE_UP_METRICS = ENABLED_TEXT
DEFAULT_ENABLE_USERS_METRICS = ENABLED_TEXT
DEFAULT_ENABLE_QUEUE_METRICS = ENABLED_TEXT

DEFAULT_WAIT_FOR_MAILMAN_SLEEP_INTERVAL_IN_SECONDS = 1


def parse_host_port(web_listen: str) -> tuple[str, int]:
    uri_info = re.split(r':', web_listen)
    match len(uri_info):
        case 0:
            hostname = DEFAULT_HOSTNAME
            port = DEFAULT_PORT
        case 1:
            hostname = uri_info[0]
            port = DEFAULT_PORT
        case 2:
            hostname = uri_info[0]
            port = int(uri_info[1])
        case _:
            logging.error(f"Listen address in unexpected form (got '{web_listen}')", )
            raise ValueError(f"listen address in unexpected form (got '{web_listen}')")
    return hostname, port


class Config:
    def __init__(self):
        self.log_level = DEFAULT_LOG_LEVEL
        self.mailman_api_version = DEFAULT_MAILMAN_API_VERSION
        self.hostname = DEFAULT_HOSTNAME
        self.port = DEFAULT_PORT
        self.mailman_address = DEFAULT_MAILMAN_ADDRESS
        self.mailman_user = DEFAULT_MAILMAN_USERNAME
        self.mailman_password = DEFAULT_MAILMAN_PASSWORD
        self.namespace = DEFAULT_NAMESPACE
        self.enable_caching = DEFAULT_CACHE_ENABLED
        self.cache_duration_in_seconds = DEFAULT_CACHE_DURATION_IN_SECONDS
        self.enable_gc_metrics = DEFAULT_ENABLE_GC_METRICS
        self.enable_platform_metrics = DEFAULT_ENABLE_PLATFORM_METRICS
        self.enable_process_metrics = DEFAULT_ENABLE_PROCESS_METRICS
        self.enable_domains_metrics = DEFAULT_ENABLE_DOMAINS_METRICS
        self.enable_lists_metrics = DEFAULT_ENABLE_LISTS_METRICS
        self.enable_up_metrics = DEFAULT_ENABLE_UP_METRICS
        self.enable_users_metrics = DEFAULT_ENABLE_USERS_METRICS
        self.enable_queue_metrics = DEFAULT_ENABLE_QUEUE_METRICS
        self.args()

    def log_config(self, prefix: str = 'config') -> None:
        no_format = lambda value: value
        obfusacte = lambda value: '*****'
        bool_to_string = lambda value: str(value).lower()
        entries = {
            'log_level': (self.log_level, no_format),
            'mailman_api_version': (self.mailman_api_version, no_format),
            'hostname': (self.hostname, no_format),
            'port': (self.port, no_format),
            'mailman_address': (self.mailman_address, no_format),
            'mailman_user': (self.mailman_user, obfusacte),
            'mailman_password': (self.mailman_password, obfusacte),
            'namespace': (self.namespace, no_format),
            'enable_caching': (self.enable_caching, bool_to_string),
            'cache_duration_in_seconds': (self.cache_duration_in_seconds, no_format),
            'enable_gc_metrics': (self.enable_gc_metrics, bool_to_string),
            'enable_platform_metrics': (self.enable_platform_metrics, bool_to_string),
            'enable_process_metrics': (self.enable_process_metrics, bool_to_string),
            'enable_domains_metrics': (self.enable_domains_metrics, bool_to_string),
            'enable_lists_metrics': (self.enable_lists_metrics, bool_to_string),
            'enable_up_metrics': (self.enable_up_metrics, bool_to_string),
            'enable_users_metrics': (self.enable_users_metrics, bool_to_string),
            'enable_queue_metrics': (self.enable_queue_metrics, bool_to_string),
        }
        for key in entries.keys():
            logging.info(f"{prefix}({key}): {entries[key][1](entries[key][0])}")

    @property
    def prefix(self) -> str:
        return f"{self.namespace}_" if self.namespace else ""

    def args(self) -> None:
        parser = ArgumentParser(description='Mailman3 Prometheus metrics exporter')

        parser.add_argument(
            '--log-level',
            dest='log_level',
            default=DEFAULT_LOG_LEVEL,
            choices=['debug', 'info', 'warning', 'error', 'critical'],
            help=f"Detail level to log. (default: {DEFAULT_LOG_LEVEL})"
        )

        parser.add_argument(
            '--log-config',
            dest='log_config',
            default=DEFAULT_LOG_CONFIG,
            choices=BOOLEAN_CHOICES,
            help="Log the current configuration except for sensitive information (log level: info). "
                 f"Can be used for debugging purposes. (default: {DEFAULT_LOG_CONFIG})"
        )

        parser.add_argument(
            '-l',
            '--web.listen',
            dest='web_listen',
            type=str,
            default=f"{DEFAULT_HOSTNAME}:{DEFAULT_PORT}",
            help=f"HTTPServer metrics listen address (default: {DEFAULT_HOSTNAME}:{DEFAULT_PORT})"
        )

        parser.add_argument(
            '-m',
            '--mailman.address',
            dest='mailman_address',
            type=str,
            default=DEFAULT_MAILMAN_ADDRESS,
            help=f"Mailman3 Core REST API address (default: {DEFAULT_MAILMAN_ADDRESS})"
        )

        parser.add_argument(
            '-u',
            '--mailman.user',
            dest='mailman_user',
            type=str,
            default=DEFAULT_MAILMAN_USERNAME,
            help=f"Mailman3 Core REST API username (default: {DEFAULT_MAILMAN_USERNAME})"
        )

        parser.add_argument(
            '-p',
            '--mailman.password',
            dest='mailman_password',
            type=str,
            default=DEFAULT_MAILMAN_PASSWORD,
            help=f"Mailman3 Core REST API password (default: {DEFAULT_MAILMAN_PASSWORD})"
        )

        parser.add_argument(
            '--namespace',
            dest='namespace',
            type=str,
            default=DEFAULT_NAMESPACE,
            help=f"Metrics namespace (default: {DEFAULT_NAMESPACE})"
        )

        parser.add_argument(
            '--cache',
            dest='enable_caching',
            type=str,
            default=DEFAULT_CACHE_ENABLED,
            choices=BOOLEAN_CHOICES,
            help=f"Enable caching (default: {DEFAULT_CACHE_ENABLED})"
        )

        parser.add_argument(
            '--cache.duration',
            dest='cache_duration',
            type=int,
            default=DEFAULT_CACHE_DURATION_IN_SECONDS,
            help=f"Cache duration in seconds (default: {DEFAULT_CACHE_DURATION_IN_SECONDS})"
        )

        parser.add_argument(
            '--metrics.gc',
            dest='enable_gc_metrics',
            type=str,
            default=DEFAULT_ENABLE_GC_METRICS,
            choices=BOOLEAN_CHOICES,
            help=f"Enable garbage collection metrics (default: {DEFAULT_ENABLE_GC_METRICS})"
        )

        parser.add_argument(
            '--metrics.platform',
            dest='enable_platform_metrics',
            type=str,
            default=DEFAULT_ENABLE_PLATFORM_METRICS,
            choices=BOOLEAN_CHOICES,
            help=f"Enable platform metrics (default: {DEFAULT_ENABLE_PLATFORM_METRICS})"
        )

        parser.add_argument(
            '--metrics.process',
            dest='enable_process_metrics',
            type=str,
            default=DEFAULT_ENABLE_PROCESS_METRICS,
            choices=BOOLEAN_CHOICES,
            help=f"Enable process metrics (default: {DEFAULT_ENABLE_PROCESS_METRICS})"
        )

        parser.add_argument(
            '--metrics.domains',
            dest='enable_domains_metrics',
            type=str,
            default=DEFAULT_ENABLE_DOMAINS_METRICS,
            choices=BOOLEAN_CHOICES,
            help=f"Enable domains metrics (default: {DEFAULT_ENABLE_DOMAINS_METRICS})"
        )

        parser.add_argument(
            '--metrics.lists',
            dest='enable_lists_metrics',
            type=str,
            default=DEFAULT_ENABLE_LISTS_METRICS,
            choices=BOOLEAN_CHOICES,
            help=f"Enable lists metrics (default: {DEFAULT_ENABLE_LISTS_METRICS})"
        )

        parser.add_argument(
            '--metrics.up',
            dest='enable_up_metrics',
            type=str,
            default=DEFAULT_ENABLE_UP_METRICS,
            choices=BOOLEAN_CHOICES,
            help=f"Enable up metrics (default: {DEFAULT_ENABLE_UP_METRICS})"
        )

        parser.add_argument(
            '--metrics.users',
            dest='enable_users_metrics',
            type=str,
            default=DEFAULT_ENABLE_USERS_METRICS,
            choices=BOOLEAN_CHOICES,
            help=f"Enable users metrics (default: {DEFAULT_ENABLE_USERS_METRICS})"
        )

        parser.add_argument(
            '--metrics.queue',
            dest='enable_queue_metrics',
            type=str,
            default=DEFAULT_ENABLE_QUEUE_METRICS,
            choices=BOOLEAN_CHOICES,
            help=f"Enable queue metrics (default: {DEFAULT_ENABLE_QUEUE_METRICS})"
        )

        args = parser.parse_args()

        log_format = '[%(asctime)s] %(name)s.%(levelname)s %(threadName)s %(message)s'
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(logging.Formatter(log_format))
        self.log_level = logging.os.environ.get('LOG_LEVEL', 'INFO')
        self.log_level = getattr(logging, args.log_level.upper(), self.log_level.upper())
        logging.basicConfig(handlers=[log_handler], level=self.log_level)
        logging.captureWarnings(True)

        self.hostname, self.port = parse_host_port(args.web_listen)
        self.mailman_address = args.mailman_address.strip('/')
        self.mailman_user = args.mailman_user
        self.mailman_password = args.mailman_password
        self.namespace = args.namespace.strip()
        self.cache_duration_in_seconds = args.cache_duration
        self.enable_caching = args.enable_caching == ENABLED_TEXT and self.cache_duration_in_seconds >= 0
        self.enable_gc_metrics = args.enable_gc_metrics == ENABLED_TEXT
        self.enable_platform_metrics = args.enable_platform_metrics == ENABLED_TEXT
        self.enable_process_metrics = args.enable_process_metrics == ENABLED_TEXT
        self.enable_domains_metrics = args.enable_domains_metrics == ENABLED_TEXT
        self.enable_lists_metrics = args.enable_lists_metrics == ENABLED_TEXT
        self.enable_up_metrics = args.enable_up_metrics == ENABLED_TEXT
        self.enable_users_metrics = args.enable_users_metrics == ENABLED_TEXT
        self.enable_queue_metrics = args.enable_queue_metrics == ENABLED_TEXT
        if args.log_config == ENABLED_TEXT:
            self.log_config()
