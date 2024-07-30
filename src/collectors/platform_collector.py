import platform as pf
from typing import Any, Iterable, Optional

from prometheus_client.core import GaugeMetricFamily, Metric
from prometheus_client.registry import (Collector, CollectorRegistry, REGISTRY)


class PlatformCollector(Collector):
    """Collector for python platform information"""

    def __init__(self,
                 namespace: str = '',
                 registry: Optional[CollectorRegistry] = REGISTRY,
                 platform: Optional[Any] = None,
                 ):
        self.prefix = f"{namespace}_" if namespace else ''
        self._platform = pf if platform is None else platform
        info = self._info()
        system = self._platform.system()
        if system == "Java":
            info.update(self._java())
        self._metrics = [
            self._add_metric(f"{self.prefix}python_info", "Python platform information", info)
        ]
        if registry:
            registry.register(self)

    def collect(self) -> Iterable[Metric]:
        return self._metrics

    @staticmethod
    def _add_metric(name, documentation, data):
        labels = data.keys()
        values = [data[k] for k in labels]
        g = GaugeMetricFamily(name, documentation, labels=labels)
        g.add_metric(values, 1)
        return g

    def _info(self):
        major, minor, patchlevel = self._platform.python_version_tuple()
        return {
            "version": self._platform.python_version(),
            "implementation": self._platform.python_implementation(),
            "major": major,
            "minor": minor,
            "patchlevel": patchlevel
        }

    def _java(self):
        java_version, _, vminfo, osinfo = self._platform.java_ver()
        vm_name, vm_release, vm_vendor = vminfo
        return {
            "jvm_version": java_version,
            "jvm_release": vm_release,
            "jvm_vendor": vm_vendor,
            "jvm_name": vm_name
        }
