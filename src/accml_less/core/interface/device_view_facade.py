"""

Todo:
    some of these should be actually protocols

"""
from abc import abstractmethod, ABCMeta
from typing import Union, Sequence

from .destination_multiplexer import DestinationMultiplexerBase
from .view import ViewR, ViewRW


class _DeviceViewFacadeSwitch(metaclass=ABCMeta):
    @abstractmethod
    def get_switching_object(self) -> DestinationMultiplexerBase:
        """
        Todo:
            add type of switching object
        """

    @abstractmethod
    def get_view_implementation(self, view_implementation_mame: str) -> Union[ViewR, ViewRW]:
        raise NotImplementedError("use derived class instead")

    @abstractmethod
    def get_view_implementation_names(self) -> Sequence[str]:
        raise NotImplementedError("use derived class instead")


class DeviceViewRFacadeBase(ViewR, _DeviceViewFacadeSwitch, metaclass=ABCMeta):
    """A common interface for wherever the information goes"""


class DeviceViewRWFacadeBase(ViewRW, _DeviceViewFacadeSwitch, metaclass=ABCMeta):
    """A common interface for wherever the information goes"""
