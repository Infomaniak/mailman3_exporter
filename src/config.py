from argparse import ArgumentParser
import logging
import re
from src.options.choices_option import ChoicesOption
from src.options.boolean_option import BooleanOption
from src.options.string_option import StringOption
from src.options.integer_option import IntegerOption

DEFAULT_MAILMAN_API_VERSION = "3.1"

DEFAULT_WAIT_FOR_MAILMAN_SLEEP_INTERVAL_IN_SECONDS = 1


def parse_host_port(web_listen: str, default_hostname: str = 'localhost', default_port: int = 9934) -> tuple[str, int]:
    uri_info = re.split(r':', web_listen)
    match len(uri_info):
        case 0:
            hostname = default_hostname
            port = default_port
        case 1:
            hostname = uri_info[0]
            port = default_port
        case 2:
            hostname = uri_info[0]
            port = int(uri_info[1])
        case _:
            logging.error(f"Listen address in unexpected form (got '{web_listen}')", )
            raise ValueError(f"listen address in unexpected form (got '{web_listen}')")
    return hostname, port


class Config:
    def __init__(self):
        log_format = '[%(asctime)s] %(name)s.%(levelname)s %(threadName)s %(message)s'
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(logging.Formatter(log_format))
        logging.basicConfig(handlers=[log_handler], level='INFO')
        logging.captureWarnings(True)
        parser = ArgumentParser(description='Mailman3 Prometheus metrics exporter')
        log_level_option = ChoicesOption(
            parser=parser,
            name='log_level',
            choices=['debug', 'info', 'warning', 'error', 'critical'],
            default_value='info',
            env_var_name='ME_LOG_LEVEL',
            help_text=f"Detail level to log. (default: info)",
            name_and_flags=['--log-level']
        )
        log_config_option = BooleanOption(
            parser=parser,
            name='log_config',
            default_value=False,
            env_var_name='ME_LOG_CONFIG',
            help_text="Log the current configuration except for sensitive information (log level: info). "
                      f"Can be used for debugging purposes. (default: false)",
            name_and_flags=['--log-config']
        )
        web_listen_option = StringOption(
            parser=parser,
            name='web_listen',
            default_value='localhost:9934',
            env_var_name='ME_WEB_LISTEN',
            help_text=f"HTTPServer metrics listen address (default: localhost:9934)",
            name_and_flags=['--web.listen']
        )
        mailman_address_option = StringOption(
            parser=parser,
            name='mailman_address',
            default_value='http://mailman-core:8001',
            env_var_name='ME_MAILMAN_ADDRESS',
            help_text=f"Mailman3 Core REST API address (default: http://mailman-core:8001)",
            name_and_flags=['--mailman.address']
        )
        mailman_user_option = StringOption(
            parser=parser,
            name='mailman_user',
            default_value='restadmin',
            env_var_name='ME_MAILMAN_USERNAME',
            help_text=f"Mailman3 Core REST API username (default: restadmin)",
            name_and_flags=['-u', '--mailman.user']
        )
        mailman_password_option = StringOption(
            parser=parser,
            name='mailman_password',
            default_value='restpass',
            env_var_name='ME_MAILMAN_PASSWORD',
            help_text=f"Mailman3 Core REST API password (default: restpass)",
            name_and_flags=['-p', '--mailman.password']
        )
        namespace_option = StringOption(
            parser=parser,
            name='namespace',
            default_value='',
            env_var_name='ME_NAMESPACE',
            help_text=f"Metrics namespace (default: <empty>)",
            name_and_flags=['--namespace']
        )
        enable_caching_option = BooleanOption(
            parser=parser,
            name='enable_caching',
            default_value=True,
            env_var_name='ME_ENABLE_CACHING',
            help_text=f"Enable caching (default: true)",
            name_and_flags=['--cache']
        )
        cache_duration_option = IntegerOption(
            parser=parser,
            name='cache_duration',
            default_value=30,
            env_var_name='ME_CACHE_DURATION_IN_SECONDS',
            help_text=f"Cache duration in seconds (default: 30)",
            name_and_flags=['--cache.duration']
        )
        enable_gc_metrics_option = BooleanOption(
            parser=parser,
            name='enable_gc_metrics',
            default_value=True,
            env_var_name='ME_ENABLE_GC_METRICS',
            help_text=f"Enable garbage collection metrics (default: true)",
            name_and_flags=['--enable-gc']
        )
        enable_platform_metrics_option = BooleanOption(
            parser=parser,
            name='enable_platform_metrics',
            default_value=True,
            env_var_name='ME_ENABLE_PLATFORM_METRICS',
            help_text=f"Enable platform metrics (default: true)",
            name_and_flags=['--metrics.platform']
        )
        enable_process_metrics_option = BooleanOption(
            parser=parser,
            name='enable_process_metrics',
            default_value=True,
            env_var_name='ME_ENABLE_PROCESS_METRICS',
            help_text=f"Enable process metrics (default: true)",
            name_and_flags=['--metrics.process']
        )
        enable_domains_metrics_option = BooleanOption(
            parser=parser,
            name='enable_domains_metrics',
            default_value=True,
            env_var_name='ME_ENABLE_DOMAINS_METRICS',
            help_text=f"Enable domains metrics (default: true)",
            name_and_flags=['--metrics.domains']
        )
        enable_lists_metrics_option = BooleanOption(
            parser=parser,
            name='enable_lists_metrics',
            default_value=True,
            env_var_name='ME_ENABLE_LISTS_METRICS',
            help_text=f"Enable lists metrics (default: true)",
            name_and_flags=['--metrics.lists']
        )
        enable_up_metrics_option = BooleanOption(
            parser=parser,
            name='enable_up_metrics',
            default_value=True,
            env_var_name='ME_ENABLE_UP_METRICS',
            help_text=f"Enable up metrics (default: true)",
            name_and_flags=['--metrics.up']
        )
        enable_users_metrics_option = BooleanOption(
            parser=parser,
            name='enable_users_metrics',
            default_value=True,
            env_var_name='ME_ENABLE_USERS_METRICS',
            help_text=f"Enable users metrics (default: true)",
            name_and_flags=['--metrics.users']
        )
        enable_queue_metrics_option = BooleanOption(
            parser=parser,
            name='enable_queue_metrics',
            default_value=True,
            env_var_name='ME_ENABLE_QUEUE_METRICS',
            help_text=f"Enable queue metrics (default: true)",
            name_and_flags=['--metrics.queue']
        )

        args = parser.parse_args()

        self.log_level = log_level_option.value(args)
        logging.basicConfig(handlers=[log_handler], level=self.log_level.upper())
        self.mailman_api_version = DEFAULT_MAILMAN_API_VERSION
        self.hostname, self.port = parse_host_port(web_listen_option.value(args))
        self.mailman_address = mailman_address_option.value(args).strip('/')
        self.mailman_user = mailman_user_option.value(args)
        self.mailman_password = mailman_password_option.value(args)
        self.namespace = namespace_option.value(args).strip()
        self.cache_duration_in_seconds = cache_duration_option.value(args)
        self.enable_caching = enable_caching_option.value(args) and self.cache_duration_in_seconds >= 0
        self.enable_gc_metrics = enable_gc_metrics_option.value(args)
        self.enable_platform_metrics = enable_platform_metrics_option.value(args)
        self.enable_process_metrics = enable_process_metrics_option.value(args)
        self.enable_domains_metrics = enable_domains_metrics_option.value(args)
        self.enable_lists_metrics = enable_lists_metrics_option.value(args)
        self.enable_up_metrics = enable_up_metrics_option.value(args)
        self.enable_users_metrics = enable_users_metrics_option.value(args)
        self.enable_queue_metrics = enable_queue_metrics_option.value(args)
        if log_config_option.value(args):
            self.log_config()

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
