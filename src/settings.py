from argparse import ArgumentParser, Namespace
import logging
import re

DEFAULT_MAILMAN_API_VERSION = "3.1"

DEFAULT_LOG_LEVEL = 'info'

DEFAULT_HOSTNAME = 'localhost'
DEFAULT_PORT = 9934

DEFAULT_MAILMAN_ADDRESS = 'http://mailman-core:8001'

DEFAULT_MAILMAN_USERNAME = 'restadmin'
DEFAULT_MAILMAN_PASSWORD = 'restpass'


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
        self.mailman_address = DEFAULT_MAILMAN_ADDRESS
        self.mailman_user = DEFAULT_MAILMAN_USERNAME
        self.mailman_password = DEFAULT_MAILMAN_PASSWORD
        self.port = DEFAULT_PORT
        self.args()

    def args(self) -> None:
        parser = ArgumentParser(description='Mailman3 Prometheus metrics exporter')

        parser.add_argument(
            '--log-level',
            default=DEFAULT_LOG_LEVEL,
            choices=['debug', 'info', 'warning', 'error', 'critical'],
            help='Detail level to log. (default: info)'
        )

        parser.add_argument(
            '-l',
            '--web.listen',
            dest='web_listen',
            type=str,
            default=f"{DEFAULT_HOSTNAME}:{DEFAULT_PORT}",
            help='HTTPServer metrics listen address'
        )

        parser.add_argument(
            '-m',
            '--mailman.address',
            dest='mailman_address',
            type=str,
            default=DEFAULT_MAILMAN_ADDRESS,
            help='Mailman3 Core REST API address'
        )

        parser.add_argument(
            '-u',
            '--mailman.user',
            dest='mailman_user',
            type=str,
            required=True,
            help='Mailman3 Core REST API username'
        )

        parser.add_argument(
            '-p',
            '--mailman.password',
            dest='mailman_password',
            type=str,
            required=True,
            help='Mailman3 Core REST API password'
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
