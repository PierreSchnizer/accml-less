import logging

from accml_less.core.interface.backend import BackendRW
from accml_less.core.interface.simulator_accelerator.accelerator_simulator import (
    AcceleratorSimulatorInterface,
)

logger = logging.getLogger()


class SimulatorBackend(BackendRW):
    def __init__(self, *, acc: AcceleratorSimulatorInterface, name: str, logger=logger):
        self.acc = acc
        self.logger = logger
        self.name = name

    def trigger(self, dev_id: str, prop_id: str):
        self.logger.info(
            "%s(name=%s) no trigger needed", self.__class__.__name__, self.name
        )

    async def read(self, dev_id: str, prop_id: str) -> object:
        elem = self.acc.get(dev_id)
        return elem.peek(prop_id)

    async def set(self, dev_id: str, prop_id: str, value: object):
        elem = self.acc.get(dev_id)
        return await elem.update(property_id=prop_id, value=value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, acc={self.acc})"
