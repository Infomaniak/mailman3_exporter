import gc
import platform
from typing import Iterable

from prometheus_client.core import CounterMetricFamily, Metric
from prometheus_client.registry import Collector, CollectorRegistry, REGISTRY


class GCCollector(Collector):
    """Collector for Garbage collection statistics."""

    def __init__(self, namespace: str = '', registry: CollectorRegistry = REGISTRY):
        self.prefix = f"{namespace}_" if namespace else ''
        if not hasattr(gc, 'get_stats') or platform.python_implementation() != 'CPython':
            return
        registry.register(self)

    def collect(self) -> Iterable[Metric]:
        collected = CounterMetricFamily(
            f"{self.prefix}python_gc_objects_collected",
            'Objects collected during gc',
            labels=['generation'],
        )
        uncollectable = CounterMetricFamily(
            f"{self.prefix}python_gc_objects_uncollectable",
            'Uncollectable objects found during GC',
            labels=['generation'],
        )

        collections = CounterMetricFamily(
            f"{self.prefix}python_gc_collections",
            'Number of times this generation was collected',
            labels=['generation'],
        )

        for gen, stat in enumerate(gc.get_stats()):
            generation = str(gen)
            collected.add_metric([generation], value=stat['collected'])
            uncollectable.add_metric([generation], value=stat['uncollectable'])
            collections.add_metric([generation], value=stat['collections'])

        return [collected, uncollectable, collections]
