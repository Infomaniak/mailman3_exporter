from argparse import ArgumentParser, Namespace
import logging
import re

ENABLED_TEXT = 'true'
DISABLED_TEXT = 'false'

DEFAULT_MAILMAN_API_VERSION = "3.1"

DEFAULT_LOG_LEVEL = 'info'

DEFAULT_HOSTNAME = 'localhost'
DEFAULT_PORT = 9934

DEFAULT_MAILMAN_ADDRESS = 'http://mailman-core:8001'

DEFAULT_MAILMAN_USERNAME = 'restadmin'
DEFAULT_MAILMAN_PASSWORD = 'restpass'

DEFAULT_CACHE_ENABLED = ENABLED_TEXT
DEFAULT_CACHE_DURATION_IN_SECONDS = 30


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


class Settings:
    def __init__(self):
        self.mailman_api_version = DEFAULT_MAILMAN_API_VERSION
        self.hostname = DEFAULT_HOSTNAME
        self.port = DEFAULT_PORT
        self.mailman_address = DEFAULT_MAILMAN_ADDRESS
        self.mailman_user = DEFAULT_MAILMAN_USERNAME
        self.mailman_password = DEFAULT_MAILMAN_PASSWORD
        self.enable_caching = DEFAULT_CACHE_ENABLED
        self.cache_duration_in_seconds = DEFAULT_CACHE_DURATION_IN_SECONDS
        self.args()

    def args(self) -> None:
        parser = ArgumentParser(description='Mailman3 Prometheus metrics exporter')

        parser.add_argument(
            '--log-level',
            default=DEFAULT_LOG_LEVEL,
            choices=['debug', 'info', 'warning', 'error', 'critical'],
            help=f"Detail level to log. (default: {DEFAULT_LOG_LEVEL})"
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
            '--cache',
            dest='enable_caching',
            type=str,
            default=DEFAULT_CACHE_ENABLED,
            choices=[ENABLED_TEXT, DISABLED_TEXT],
            help=f"Enable caching (default: {DEFAULT_CACHE_ENABLED})"
        )

        parser.add_argument(
            '--cache.duration',
            dest='cache_duration',
            type=int,
            default=DEFAULT_CACHE_DURATION_IN_SECONDS,
            help=f"Cache duration in seconds (default: {DEFAULT_CACHE_DURATION_IN_SECONDS})"
        )

        args = parser.parse_args()

        log_format = '[%(asctime)s] %(name)s.%(levelname)s %(threadName)s %(message)s'
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(logging.Formatter(log_format))
        log_level = logging.os.environ.get('LOG_LEVEL', 'INFO')
        log_level = getattr(logging, args.log_level.upper(), log_level.upper())
        logging.basicConfig(handlers=[log_handler], level=log_level)
        logging.captureWarnings(True)

        self.hostname, self.port = parse_host_port(args.web_listen)
        self.mailman_address = args.mailman_address
        self.mailman_user = args.mailman_user
        self.mailman_password = args.mailman_password
        self.cache_duration_in_seconds = args.cache_duration
        self.enable_caching = args.enable_caching == ENABLED_TEXT and self.cache_duration_in_seconds >= 0
