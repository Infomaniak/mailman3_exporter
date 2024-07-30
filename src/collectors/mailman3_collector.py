from prometheus_client.registry import Collector, CollectorRegistry, REGISTRY
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily
from src.metric_processing_time import metric_processing_time
import logging
from src.api import Api
from src.cache import Cache
from src.config import Config


class Mailman3Collector(Collector):

    def __init__(self, api: Api, config: Config, registry: CollectorRegistry = REGISTRY):
        self.api = api
        self.config = config
        self.cache = Cache(api, config)

        if registry:
            registry.register(self)

    def collect_domains(self, processing_time: GaugeMetricFamily) -> None:
        with metric_processing_time('domains', processing_time):
            mailman3_domains = GaugeMetricFamily(f"{self.config.prefix}mailman3_domains", 'Number of configured list domains')
            domains_status, domains = self.cache.domains()
            if 200 <= domains_status < 220:
                mailman3_domains.add_metric(['count'], domains['total_size'])
            else:
                mailman3_domains.add_metric(['count'], 0)
            yield mailman3_domains

    def collect_lists(self, processing_time: GaugeMetricFamily) -> None:
        with metric_processing_time('lists', processing_time):
            mailman3_lists = GaugeMetricFamily(f"{self.config.prefix}mailman3_lists", 'Number of configured lists')
            no_lists = False
            lists_status, lists = self.cache.lists()
            if 200 <= lists_status < 220:
                mailman3_lists.add_metric(['count'], lists['total_size'])
            else:
                mailman3_lists.add_metric(['count'], 0)
                no_lists = True
            yield mailman3_lists

            mlabels = ['list']
            if not no_lists:
                for e in lists['entries']:
                    logging.debug("members: label %s" % e['fqdn_listname'])
                    mlabels.append(e['fqdn_listname'])
            mailman3_list_members = CounterMetricFamily(f"{self.config.prefix}mailman3_list_members", 'Count members per list',
                                                        labels=mlabels)
            if not no_lists:
                for e in lists['entries']:
                    logging.debug("members metric %s value %s", e['fqdn_listname'], str(e['member_count']))
                    mailman3_list_members.add_metric([e['fqdn_listname']], value=e['member_count'])
            yield mailman3_list_members

    def collect_up(self, processing_time: GaugeMetricFamily) -> None:
        with metric_processing_time('up', processing_time):
            mailman3_up = GaugeMetricFamily(f"{self.config.prefix}mailman3_up", 'Status of mailman-core; 1 if accessible, 0 otherwise')
            status, resp = self.api.versions()
            if 200 <= status < 220:
                mailman3_up.add_metric(['up'], 1)
            else:
                mailman3_up.add_metric(['up'], 0)
            yield mailman3_up

    def collect_users(self, processing_time: GaugeMetricFamily) -> None:
        with metric_processing_time('users', processing_time):
            mailman3_users = CounterMetricFamily(f"{self.config.prefix}mailman3_users", 'Number of list users recorded in mailman-core')
            status, resp = self.api.usercount()
            if 200 <= status < 220:
                mailman3_users.add_metric(['count'], resp['total_size'])
            else:
                mailman3_users.add_metric(['count'], 0)
            yield mailman3_users

    def collect_queue(self, processing_time: GaugeMetricFamily) -> None:
        with metric_processing_time('queue', processing_time):
            qlabels = ['queue',
                       "archive", "bad", "bounces", "command",
                       "digest", "in", "nntp", "out", "pipeline",
                       "retry", "shunt", "virgin"
                       ]
            mailman3_queue = GaugeMetricFamily(f"{self.config.prefix}mailman3_queues", 'Queue length for mailman-core internal queues',
                                               labels=qlabels)
            mailman3_queue_status = GaugeMetricFamily(f"{self.config.prefix}mailman3_queues_status", 'HTTP code for queue status request')
            status, resp = self.api.queues()
            if 200 <= status < 220:
                for e in resp['entries']:
                    logging.debug("queue metric %s value %s", e['name'], str(e['count']))
                    mailman3_queue.add_metric([e['name']], value=e['count'])
                mailman3_queue_status.add_metric(['status'], value=status)
            else:
                mailman3_queue_status.add_metric(['status'], value=status)
            yield mailman3_queue

    def proc_labels(self):
        labels = [
            ('up', self.config.enable_up_metrics),
            ('queue', self.config.enable_queue_metrics),
            ('domains', self.config.enable_domains_metrics),
            ('lists', self.config.enable_lists_metrics),
            ('users', self.config.enable_users_metrics),
        ]
        labels = filter(lambda label: label[1] is True, labels)
        return ['method', *[label[0] for label in labels]]

    def collect(self) -> None:
        processing_time = GaugeMetricFamily(f"{self.config.prefix}processing_time_ms", 'Time taken to collect metrics', labels=self.proc_labels())

        self.cache.refresh_time()

        if self.config.enable_domains_metrics:
            yield from self.collect_domains(processing_time)
        if self.config.enable_lists_metrics:
            yield from self.collect_lists(processing_time)
        if self.config.enable_up_metrics:
            yield from self.collect_up(processing_time)
        if self.config.enable_users_metrics:
            yield from self.collect_users(processing_time)
        if self.config.enable_queue_metrics:
            yield from self.collect_queue(processing_time)
        yield processing_time
