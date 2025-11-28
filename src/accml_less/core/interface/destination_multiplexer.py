from abc import ABCMeta, abstractmethod


class DestinationMultiplexer(metaclass=ABCMeta):
    """Allows setting to which destination the data should go"""

    @abstractmethod
    def set_target(self, target_name: str):
        raise NotImplementedError("Use derived class instead")

    @abstractmethod
    def get_target_name(self) -> str:
        raise NotImplementedError("Use derived class instead")
