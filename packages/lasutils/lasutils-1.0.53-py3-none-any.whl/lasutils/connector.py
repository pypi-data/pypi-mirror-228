import logging
import signal
from abc import ABC, abstractmethod
from importlib import import_module
from lasutils import settings, exceptions

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Connector(ABC):
    def __init__(self):
        self.shutdown = False
        signal.signal(signal.SIGINT, self._exit_gracefully)
        signal.signal(signal.SIGTERM, self._exit_gracefully)
        self.config = settings.CONFIG
        self.secrets = settings.SECRETS

    def _exit_gracefully(self, signum, frame):
        signal_name = "SIGTERM" if signum == signal.SIGTERM else "SIGINT"
        logger.info(f"Received {signal_name}, waiting for running tasks to finish...")
        self.shutdown = True

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass


def run_connector():
    """Runs connector class specified as dotted list"""
    if not settings.POLLER_CLASS:
        raise exceptions.MissingEnvironmentVariable("CLASS")

    mod_name, cls_name = settings.POLLER_CLASS.rsplit(".", 1)
    cls = getattr(import_module(mod_name), cls_name)
    assert issubclass(cls, Connector)

    app = cls()
    app.start()
    while not app.shutdown:
        app.run()
    app.stop()
