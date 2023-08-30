import itertools
import os
from typing import ClassVar
from typing import Optional
from typing import Set

import attr

import ddtrace
from ddtrace.internal import atexit
from ddtrace.internal import forksafe

from .. import periodic
from ..dogstatsd import get_dogstatsd_client
from ..logger import get_logger
from .constants import DEFAULT_RUNTIME_METRICS
from .metric_collectors import GCRuntimeMetricCollector
from .metric_collectors import PSUtilRuntimeMetricCollector
from .tag_collectors import PlatformTagCollector
from .tag_collectors import TracerTagCollector


log = get_logger(__name__)


class RuntimeCollectorsIterable(object):
    def __init__(self, enabled=None):
        self._enabled = enabled or self.ENABLED
        # Initialize the collectors.
        self._collectors = [c() for c in self.COLLECTORS]

    def __iter__(self):
        collected = (collector.collect(self._enabled) for collector in self._collectors)
        return itertools.chain.from_iterable(collected)

    def __repr__(self):
        return "{}(enabled={})".format(
            self.__class__.__name__,
            self._enabled,
        )


class RuntimeTags(RuntimeCollectorsIterable):
    # DEV: `None` means to allow all tags generated by PlatformTagCollector and TracerTagCollector
    ENABLED = None
    COLLECTORS = [
        PlatformTagCollector,
        TracerTagCollector,
    ]


class RuntimeMetrics(RuntimeCollectorsIterable):
    ENABLED = DEFAULT_RUNTIME_METRICS
    COLLECTORS = [
        GCRuntimeMetricCollector,
        PSUtilRuntimeMetricCollector,
    ]


def _get_interval_or_default():
    return float(os.getenv("DD_RUNTIME_METRICS_INTERVAL", default=10))


@attr.s(eq=False)
class RuntimeWorker(periodic.PeriodicService):
    """Worker thread for collecting and writing runtime metrics to a DogStatsd
    client.
    """

    _interval = attr.ib(type=float, factory=_get_interval_or_default)
    tracer = attr.ib(type=ddtrace.Tracer, default=None)
    dogstatsd_url = attr.ib(type=Optional[str], default=None)
    _dogstatsd_client = attr.ib(init=False, repr=False)
    _runtime_metrics = attr.ib(factory=RuntimeMetrics, repr=False)
    _services = attr.ib(type=Set[str], init=False, factory=set)

    enabled = False
    _instance = None  # type: ClassVar[Optional[RuntimeWorker]]
    _lock = forksafe.Lock()

    def __attrs_post_init__(self):
        # type: () -> None
        self._dogstatsd_client = get_dogstatsd_client(self.dogstatsd_url or ddtrace.internal.agent.get_stats_url())
        self.tracer = self.tracer or ddtrace.tracer

    @classmethod
    def disable(cls):
        # type: () -> None
        with cls._lock:
            if cls._instance is None:
                return

            forksafe.unregister(cls._restart)

            cls._instance.stop()
            # DEV: Use timeout to avoid locking on shutdown. This seems to be
            # required on some occasions by Python 2.7. Deadlocks seem to happen
            # when some functionalities (e.g. platform.architecture) are used
            # which end up calling
            #    _execute_child (/usr/lib/python2.7/subprocess.py:1023)
            # This is a continuous attempt to read:
            #    _eintr_retry_call (/usr/lib/python2.7/subprocess.py:125)
            # which is the eventual cause of the deadlock.
            cls._instance.join(1)
            cls._instance = None
            cls.enabled = False

    @classmethod
    def _restart(cls):
        cls.disable()
        cls.enable()

    @classmethod
    def enable(cls, flush_interval=None, tracer=None, dogstatsd_url=None):
        # type: (Optional[float], Optional[ddtrace.Tracer], Optional[str]) -> None
        with cls._lock:
            if cls._instance is not None:
                return
            if flush_interval is None:
                flush_interval = _get_interval_or_default()
            runtime_worker = cls(flush_interval, tracer, dogstatsd_url)  # type: ignore[arg-type]
            runtime_worker.start()
            # force an immediate update constant tags
            runtime_worker.update_runtime_tags()

            forksafe.register(cls._restart)
            atexit.register(cls.disable)

            cls._instance = runtime_worker
            cls.enabled = True

    def flush(self):
        # type: () -> None
        # The constant tags for the dogstatsd client needs to updated with any new
        # service(s) that may have been added.
        if self._services != self.tracer._services:
            self._services = self.tracer._services
            self.update_runtime_tags()

        with self._dogstatsd_client:
            for key, value in self._runtime_metrics:
                log.debug("Writing metric %s:%s", key, value)
                self._dogstatsd_client.distribution(key, value)

    def _stop_service(self):
        # type: (...) -> None
        # De-register span hook
        super(RuntimeWorker, self)._stop_service()

    def update_runtime_tags(self):
        # type: () -> None
        # DEV: ddstatsd expects tags in the form ['key1:value1', 'key2:value2', ...]
        tags = ["{}:{}".format(k, v) for k, v in RuntimeTags()]
        log.debug("Updating constant tags %s", tags)
        self._dogstatsd_client.constant_tags = tags

    periodic = flush
    on_shutdown = flush
