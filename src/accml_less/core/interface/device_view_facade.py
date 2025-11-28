"""

Todo:
    some of these should be actually protocols

"""
from abc import abstractmethod, ABCMeta

from accml_less.core.interface.destination_multiplexer import DestinationMultiplexer
from accml_less.core.interface.view import ViewR, ViewRW


class _DeviceViewFacadeSwitch(metaclass=ABCMeta):
    @abstractmethod
    def get_switching_object(self) -> DestinationMultiplexer:
        """
        Todo:
            add type of switching object
        """


class DeviceViewRFacadeBase(ViewR, _DeviceViewFacadeSwitch, metaclass=ABCMeta):
    """A common interface for wherever the information goes"""


class DeviceViewRWFacadeBase(ViewRW, _DeviceViewFacadeSwitch, metaclass=ABCMeta):
    """A common interface for wherever the information goes"""
